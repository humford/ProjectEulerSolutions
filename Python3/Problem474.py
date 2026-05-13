from collections import defaultdict
import math
import time


MODULUS = 10**16 + 61
PROBLEM_N = 10**6
PROBLEM_DIGITS = 65432


def primeSieve(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for factor in range(2, math.isqrt(limit) + 1):
        if sieve[factor]:
            start = factor * factor
            sieve[start:limit + 1:factor] = (
                b"\x00" * (((limit - start) // factor) + 1)
            )

    return [number for number in range(2, limit + 1) if sieve[number]]


def factorialPrimeExponent(n, prime):
    exponent = 0
    while n:
        n //= prime
        exponent += n
    return exponent


def primePowerExponent(value, prime):
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def lcm(left, right):
    return left // math.gcd(left, right) * right


def distinctPrimeFactors(value):
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitiveRootFivePower(modulus):
    phi = modulus - modulus // 5
    tests = distinctPrimeFactors(phi)

    for candidate in range(2, modulus):
        if math.gcd(candidate, modulus) != 1:
            continue
        if all(pow(candidate, phi // factor, modulus) != 1 for factor in tests):
            return candidate

    raise ValueError("primitive root not found")


LOG_TABLE_CACHE = {}


def fivePowerLogTable(exponent):
    if exponent in LOG_TABLE_CACHE:
        return LOG_TABLE_CACHE[exponent]

    if exponent == 0:
        result = (1, [0])
        LOG_TABLE_CACHE[exponent] = result
        return result

    modulus = 5**exponent
    groupOrder = 4 * 5 ** (exponent - 1)
    generator = primitiveRootFivePower(modulus)
    logs = [-1] * modulus
    value = 1

    for logValue in range(groupOrder):
        logs[value] = logValue
        value = value * generator % modulus

    result = (modulus, logs)
    LOG_TABLE_CACHE[exponent] = result
    return result


TWO_POWER_MAP_CACHE = {}


def twoPowerUnitMap(exponent):
    if exponent in TWO_POWER_MAP_CACHE:
        return TWO_POWER_MAP_CACHE[exponent]

    modulus = 1 << exponent
    if exponent <= 1:
        units = [(-1, -1)] * modulus
        units[1 % modulus] = (0, 0)
        result = (1, 1, units)
        TWO_POWER_MAP_CACHE[exponent] = result
        return result

    if exponent == 2:
        units = [(-1, -1)] * modulus
        units[1] = (0, 0)
        units[3] = (1, 0)
        result = (2, 1, units)
        TWO_POWER_MAP_CACHE[exponent] = result
        return result

    signModulus = 2
    powerModulus = 1 << (exponent - 2)
    units = [(-1, -1)] * modulus
    for signExponent in range(signModulus):
        sign = -1 if signExponent else 1
        for powerExponent in range(powerModulus):
            value = sign * pow(5, powerExponent, modulus) % modulus
            units[value] = (signExponent, powerExponent)

    result = (signModulus, powerModulus, units)
    TWO_POWER_MAP_CACHE[exponent] = result
    return result


def multiplyByPrimeChoices(distribution, prime, exponent, twoExponent,
                           fiveExponent):
    signModulus, powerModulus, units2 = twoPowerUnitMap(twoExponent)
    modulus2 = 1 << twoExponent if twoExponent > 0 else 1
    modulus5, logs5 = fivePowerLogTable(fiveExponent)
    logModulus = 1 if fiveExponent == 0 else 4 * 5 ** (fiveExponent - 1)

    if twoExponent > 0:
        signStep, powerStep = units2[prime % modulus2]
    else:
        signStep, powerStep = 0, 0

    if fiveExponent > 0:
        logStep = logs5[prime % modulus5]
    else:
        logStep = 0

    if signStep == 0 and powerStep == 0 and logStep == 0:
        multiplier = (exponent + 1) % MODULUS
        for signIndex in range(signModulus):
            for powerIndex in range(powerModulus):
                row = distribution[signIndex][powerIndex]
                for logIndex in range(logModulus):
                    row[logIndex] = row[logIndex] * multiplier % MODULUS
        return distribution

    signOrder = 1 if signModulus == 1 or signStep == 0 else 2
    powerOrder = (
        1 if powerModulus == 1 or powerStep == 0
        else powerModulus // math.gcd(powerStep, powerModulus)
    )
    logOrder = (
        1 if logModulus == 1 or logStep == 0
        else logModulus // math.gcd(logStep, logModulus)
    )
    cycleLength = lcm(lcm(signOrder, powerOrder), logOrder)
    fullCycles, remainder = divmod(exponent + 1, cycleLength)

    nextDistribution = [
        [[0] * logModulus for _ in range(powerModulus)]
        for _ in range(signModulus)
    ]

    for residue in range(cycleLength):
        choiceCount = fullCycles + (1 if residue < remainder else 0)
        if choiceCount == 0:
            continue

        signDelta = signStep * residue % signModulus if signModulus > 1 else 0
        powerDelta = (
            powerStep * residue % powerModulus if powerModulus > 1 else 0
        )
        logDelta = logStep * residue % logModulus if logModulus > 1 else 0
        choiceCount %= MODULUS

        for signIndex in range(signModulus):
            signTarget = (signIndex + signDelta) % signModulus
            for powerIndex in range(powerModulus):
                powerTarget = (powerIndex + powerDelta) % powerModulus
                source = distribution[signIndex][powerIndex]
                target = nextDistribution[signTarget][powerTarget]

                if logDelta == 0:
                    for logIndex in range(logModulus):
                        target[logIndex] = (
                            target[logIndex] + choiceCount * source[logIndex]
                        ) % MODULUS
                else:
                    for logIndex in range(logModulus):
                        target[(logIndex + logDelta) % logModulus] = (
                            target[(logIndex + logDelta) % logModulus]
                            + choiceCount * source[logIndex]
                        ) % MODULUS

    return nextDistribution


DP_CACHE = {}


def unitPartDistribution(primes, exponents, twoExponent, fiveExponent):
    key = (twoExponent, fiveExponent)
    if key in DP_CACHE:
        return DP_CACHE[key]

    signModulus, powerModulus, _ = twoPowerUnitMap(twoExponent)
    logModulus = 1 if fiveExponent == 0 else 4 * 5 ** (fiveExponent - 1)
    distribution = [
        [[0] * logModulus for _ in range(powerModulus)]
        for _ in range(signModulus)
    ]
    distribution[0][0][0] = 1

    for prime in primes:
        if prime in (2, 5):
            continue
        distribution = multiplyByPrimeChoices(
            distribution,
            prime,
            exponents[prime],
            twoExponent,
            fiveExponent,
        )

    DP_CACHE[key] = distribution
    return distribution


def combineResidues(residue2, twoExponent, residue5, fiveExponent):
    if twoExponent == 0:
        return residue5
    if fiveExponent == 0:
        return residue2

    modulus2 = 1 << twoExponent
    modulus5 = 5**fiveExponent
    return (
        residue2
        + modulus2 * ((residue5 - residue2) * pow(modulus2, -1, modulus5)
                      % modulus5)
    ) % (modulus2 * modulus5)


def targetUnitResidue(digits, twoCount, fiveCount, twoExponent, fiveExponent):
    digitCount = len(str(digits))
    modulus2Full = 1 << digitCount
    modulus5Full = 5**digitCount

    if twoExponent > 0:
        inverse5 = pow(pow(5, fiveCount, modulus2Full), -1, modulus2Full)
        residue2Full = digits * inverse5 % modulus2Full
        residue2 = (residue2Full >> twoCount) % (1 << twoExponent)
    else:
        residue2 = 0

    if fiveExponent > 0:
        inverse2 = pow(pow(2, twoCount, modulus5Full), -1, modulus5Full)
        residue5Full = digits * inverse2 % modulus5Full
        residue5 = (residue5Full // (5**fiveCount)) % (5**fiveExponent)
    else:
        residue5 = 0

    return combineResidues(residue2, twoExponent, residue5, fiveExponent)


def targetDistributionIndex(residue, twoExponent, fiveExponent):
    if twoExponent > 0:
        signIndex, powerIndex = twoPowerUnitMap(twoExponent)[2][
            residue % (1 << twoExponent)
        ]
        if signIndex < 0:
            return None
    else:
        signIndex, powerIndex = 0, 0

    if fiveExponent > 0:
        modulus5, logs5 = fivePowerLogTable(fiveExponent)
        logIndex = logs5[residue % modulus5]
        if logIndex < 0:
            return None
    else:
        logIndex = 0

    return signIndex, powerIndex, logIndex


def divisorSuffixCount(n, digits):
    digitCount = len(str(digits))
    digitTwoExponent = primePowerExponent(digits, 2)
    digitFiveExponent = primePowerExponent(digits, 5)

    primes = primeSieve(n)
    exponents = {
        prime: factorialPrimeExponent(n, prime)
        for prime in primes
    }
    factorialTwoExponent = exponents.get(2, 0)
    factorialFiveExponent = exponents.get(5, 0)

    if digitTwoExponent < digitCount:
        twoChoices = [digitTwoExponent]
    else:
        twoChoices = range(digitCount, factorialTwoExponent + 1)

    if digitFiveExponent < digitCount:
        fiveChoices = [digitFiveExponent]
    else:
        fiveChoices = range(digitCount, factorialFiveExponent + 1)

    total = 0
    for twoCount in twoChoices:
        if twoCount > factorialTwoExponent:
            continue
        for fiveCount in fiveChoices:
            if fiveCount > factorialFiveExponent:
                continue

            twoExponent = 0 if twoCount >= digitCount else digitCount - twoCount
            fiveExponent = (
                0 if fiveCount >= digitCount else digitCount - fiveCount
            )
            targetResidue = targetUnitResidue(
                digits, twoCount, fiveCount, twoExponent, fiveExponent
            )
            index = targetDistributionIndex(
                targetResidue, twoExponent, fiveExponent
            )
            if index is None:
                continue

            distribution = unitPartDistribution(
                primes, exponents, twoExponent, fiveExponent
            )
            signIndex, powerIndex, logIndex = index
            total += distribution[signIndex][powerIndex][logIndex]

    return total % MODULUS


def integerDivisorSuffixCount(value, digits):
    modulus = 10 ** len(str(digits))
    count = 0
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor:
            continue

        if divisor % modulus == digits:
            count += 1
        quotient = value // divisor
        if quotient != divisor and quotient % modulus == digits:
            count += 1

    return count


def factorialDivisorSuffixCountBrute(n, digits):
    modulus = 10 ** len(str(digits))
    counts = defaultdict(int)
    counts[1 % modulus] = 1

    for prime in primeSieve(n):
        exponent = factorialPrimeExponent(n, prime)
        powers = []
        value = 1
        for _ in range(exponent + 1):
            powers.append(value)
            value = value * prime % modulus

        nextCounts = defaultdict(int)
        for residue, count in counts.items():
            for power in powers:
                nextCounts[residue * power % modulus] += count
        counts = nextCounts

    return counts[digits]


def runTests():
    assert integerDivisorSuffixCount(84, 4) == 3
    assert divisorSuffixCount(12, 12) == 11
    assert divisorSuffixCount(50, 123) == 17_888
    assert divisorSuffixCount(20, 34) == factorialDivisorSuffixCountBrute(20, 34)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisorSuffixCount(PROBLEM_N, PROBLEM_DIGITS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
