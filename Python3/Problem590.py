import itertools
import math
import time
from collections import Counter


MODULUS = 10 ** 9
FIVE_POWER_PART = 5 ** 9
POWER_PERIOD = 4 * 5 ** 8
INVERSE_TWO_POWER_PART = pow(2 ** 9, -1, FIVE_POWER_PART)


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0

    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (((limit - start) // prime) + 1)

    return [value for value in range(2, limit + 1) if sieve[value]]


def lcmPrimeExponentCounts(limit):
    counts = Counter()
    for prime in primesUpTo(limit):
        exponent = 0
        power = prime
        while power <= limit:
            exponent += 1
            power *= prime
        counts[exponent] += 1

    return counts


def _divisors(n):
    return [divisor for divisor in range(1, n + 1) if n % divisor == 0]


def lcmSetCount(n):
    divisors = _divisors(n)
    total = 0
    for mask in range(1, 1 << len(divisors)):
        lcm = 1
        for index, divisor in enumerate(divisors):
            if mask & (1 << index):
                lcm = lcm * divisor // math.gcd(lcm, divisor)
        if lcm == n:
            total += 1

    return total


def powerOfTwoResidueTable():
    table = [0] * POWER_PERIOD
    fivePowerResidue = 1
    for exponentResidue in range(POWER_PERIOD):
        table[exponentResidue] = (
            (2 ** 9)
            * ((fivePowerResidue * INVERSE_TWO_POWER_PART) % FIVE_POWER_PART)
        ) % MODULUS
        fivePowerResidue = (2 * fivePowerResidue) % FIVE_POWER_PART

    return table


POWER_OF_TWO_RESIDUES = powerOfTwoResidueTable()


def powerOfTwoMod(exponent):
    if exponent < 9:
        return pow(2, exponent, MODULUS)
    return POWER_OF_TWO_RESIDUES[exponent % POWER_PERIOD]


def signedBinomialCoefficients(count):
    coefficients = []
    binomial = 1
    for unselected in range(count + 1):
        selected = count - unselected
        coefficient = binomial % MODULUS
        if selected % 2:
            coefficient = -coefficient
        coefficients.append(coefficient % MODULUS)

        if unselected < count:
            binomial = binomial * (count - unselected) // (unselected + 1)

    return coefficients


def directHl(limit):
    exponents = []
    for exponent, count in lcmPrimeExponentCounts(limit).items():
        exponents.extend([exponent] * count)

    total = 0
    for mask in range(1 << len(exponents)):
        divisorCount = 1
        selectedCount = 0
        for index, exponent in enumerate(exponents):
            if mask & (1 << index):
                selectedCount += 1
                divisorCount *= exponent
            else:
                divisorCount *= exponent + 1

        term = powerOfTwoMod(divisorCount)
        if selectedCount % 2:
            total -= term
        else:
            total += term

    return total % MODULUS


def groupedHl(limit):
    exponentCounts = lcmPrimeExponentCounts(limit)
    exponentOneCount = exponentCounts.pop(1, 0)
    exponentOneCoefficients = signedBinomialCoefficients(exponentOneCount)

    powersOfTwo = [1] * (exponentOneCount + 1)
    for index in range(1, exponentOneCount + 1):
        powersOfTwo[index] = (2 * powersOfTwo[index - 1]) % POWER_PERIOD

    oneExponentCache = {}

    def sumOverExponentOnePrimes(baseExponent):
        baseExponent %= POWER_PERIOD
        if baseExponent in oneExponentCache:
            return oneExponentCache[baseExponent]

        total = 0
        for unselected, coefficient in enumerate(exponentOneCoefficients):
            exponentResidue = (baseExponent * powersOfTwo[unselected]) % POWER_PERIOD
            total += coefficient * POWER_OF_TWO_RESIDUES[exponentResidue]

        oneExponentCache[baseExponent] = total % MODULUS
        return oneExponentCache[baseExponent]

    groupedOptions = []
    for exponent, count in exponentCounts.items():
        options = []
        binomial = 1
        for selected in range(count + 1):
            coefficient = binomial % MODULUS
            if selected % 2:
                coefficient = -coefficient

            exponentFactor = (
                pow(exponent, selected, POWER_PERIOD)
                * pow(exponent + 1, count - selected, POWER_PERIOD)
            ) % POWER_PERIOD
            options.append((coefficient % MODULUS, exponentFactor))

            if selected < count:
                binomial = binomial * (count - selected) // (selected + 1)

        groupedOptions.append(options)

    total = 0
    for choices in itertools.product(*groupedOptions):
        coefficient = 1
        baseExponent = 1
        for choiceCoefficient, exponentFactor in choices:
            coefficient = (coefficient * choiceCoefficient) % MODULUS
            baseExponent = (baseExponent * exponentFactor) % POWER_PERIOD
        total += coefficient * sumOverExponentOnePrimes(baseExponent)

    return total % MODULUS


def hl(limit):
    if sum(lcmPrimeExponentCounts(limit).values()) <= 20:
        return directHl(limit)
    return groupedHl(limit)


def runTests():
    assert lcmSetCount(6) == 10
    assert hl(4) == 44


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hl(50_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
