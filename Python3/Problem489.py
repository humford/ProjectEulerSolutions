import math
import time


def primeSieve(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start:limit + 1:number] = b"\x00" * ((limit - start) // number + 1)

    return [number for number in range(limit + 1) if sieve[number]]


PRIMES = primeSieve(12_000)


def modularInverse(value, modulus):
    return pow(value, -1, modulus)


def tonelliShanks(value, prime):
    value %= prime
    if value == 0:
        return 0
    if prime == 2:
        return value
    if pow(value, (prime - 1) // 2, prime) != 1:
        return None
    if prime % 4 == 3:
        return pow(value, (prime + 1) // 4, prime)

    oddPart = prime - 1
    twos = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        twos += 1

    nonResidue = 2
    while pow(nonResidue, (prime - 1) // 2, prime) != prime - 1:
        nonResidue += 1

    exponent = twos
    factor = pow(nonResidue, oddPart, prime)
    current = pow(value, oddPart, prime)
    root = pow(value, (oddPart + 1) // 2, prime)

    while current != 1:
        index = 1
        squared = current * current % prime
        while index < exponent and squared != 1:
            squared = squared * squared % prime
            index += 1

        adjustment = pow(factor, 1 << (exponent - index - 1), prime)
        root = root * adjustment % prime
        factor = adjustment * adjustment % prime
        current = current * factor % prime
        exponent = index

    return root


def factorizeSmall(n):
    factors = {}
    remaining = n

    for prime in PRIMES:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            factors[prime] = exponent

    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1

    return factors


def initialSolutionsModPrime(a, b, prime):
    bMod = b % prime

    if a % prime == 0:
        return [
            n for n in range(prime)
            if (pow(n, 3, prime) + bMod) % prime == 0
            and (pow(n + a, 3, prime) + bMod) % prime == 0
        ]

    if prime == 3:
        return []

    if prime == 2:
        return [
            n for n in range(2)
            if (n ** 3 + b) % 2 == 0 and ((n + a) ** 3 + b) % 2 == 0
        ]

    aMod = a % prime
    discriminant = (-3 * aMod * aMod) % prime
    squareRoot = tonelliShanks(discriminant, prime)
    if squareRoot is None:
        return []

    inverse6 = modularInverse(6 % prime, prime)
    base = (-3 * aMod) % prime
    candidates = {
        (base + squareRoot) * inverse6 % prime,
        (base - squareRoot) * inverse6 % prime,
    }

    return sorted(
        n for n in candidates
        if (pow(n, 3, prime) + bMod) % prime == 0
        and (pow(n + a, 3, prime) + bMod) % prime == 0
    )


def linearSolutionsModPrime(coefficient, value, prime):
    coefficient %= prime
    value %= prime

    if coefficient == 0:
        return list(range(prime)) if value == 0 else []

    return [value * modularInverse(coefficient, prime) % prime]


def solutionsForPrimePower(a, b, prime, maxExponent):
    if maxExponent <= 0:
        return 0, []

    solutions = initialSolutionsModPrime(a, b, prime)
    if not solutions:
        return 0, []

    modulus = prime
    exponent = 1

    while exponent < maxExponent:
        nextModulus = modulus * prime
        nextSolutions = set()

        for residue in solutions:
            firstValue = (pow(residue, 3, nextModulus) + b) % nextModulus
            secondValue = (pow(residue + a, 3, nextModulus) + b) % nextModulus
            if firstValue % modulus != 0 or secondValue % modulus != 0:
                continue

            firstCoefficient = 3 * (residue % prime) ** 2 % prime
            secondCoefficient = 3 * ((residue + a) % prime) ** 2 % prime
            firstTarget = -(firstValue // modulus) % prime
            secondTarget = -(secondValue // modulus) % prime

            firstLifts = linearSolutionsModPrime(firstCoefficient, firstTarget, prime)
            secondLifts = linearSolutionsModPrime(secondCoefficient, secondTarget, prime)
            if not firstLifts or not secondLifts:
                continue

            if len(firstLifts) == prime and len(secondLifts) == prime:
                lifts = range(prime)
            elif len(firstLifts) == prime:
                lifts = secondLifts
            elif len(secondLifts) == prime:
                lifts = firstLifts
            else:
                lifts = firstLifts if firstLifts[0] == secondLifts[0] else []

            for lift in lifts:
                nextSolutions.add(residue + lift * modulus)

        if not nextSolutions:
            break

        solutions = sorted(nextSolutions)
        modulus = nextModulus
        exponent += 1

    return exponent, solutions


def combineCongruences(firstSolutions, firstModulus, secondSolutions, secondModulus):
    if firstModulus == 1:
        return sorted({solution % secondModulus for solution in secondSolutions}), secondModulus
    if secondModulus == 1:
        return sorted({solution % firstModulus for solution in firstSolutions}), firstModulus

    inverseFirst = modularInverse(firstModulus % secondModulus, secondModulus)
    combinedModulus = firstModulus * secondModulus
    solutions = set()

    for first in firstSolutions:
        first %= firstModulus
        for second in secondSolutions:
            second %= secondModulus
            multiplier = (second - first) % secondModulus
            multiplier = multiplier * inverseFirst % secondModulus
            solutions.add(first + firstModulus * multiplier)

    return sorted(solutions), combinedModulus


def precomputeAData(maxA):
    powers3 = [0] * (maxA + 1)
    powers6 = [0] * (maxA + 1)
    factors = [{} for _ in range(maxA + 1)]

    for a in range(1, maxA + 1):
        powers3[a] = a ** 3
        powers6[a] = a ** 6
        factors[a] = factorizeSmall(a)

    return powers3, powers6, factors


A3, A6, A_FACTORS = precomputeAData(18)


def commonFactorLeastN(a, b):
    resultantPart = A6[a] + 27 * b * b
    factors = factorizeSmall(resultantPart)

    for prime, exponent in A_FACTORS[a].items():
        factors[prime] = factors.get(prime, 0) + 3 * exponent

    congruenceBlocks = []
    for prime, maxExponent in factors.items():
        exponent, solutions = solutionsForPrimePower(a, b, prime, maxExponent)
        if exponent > 0:
            congruenceBlocks.append((prime, exponent, solutions))

    if not congruenceBlocks:
        return 0

    solutions = [0]
    modulus = 1
    for prime, exponent, primeSolutions in sorted(congruenceBlocks):
        solutions, modulus = combineCongruences(
            solutions,
            modulus,
            primeSolutions,
            prime ** exponent,
        )

    return min(solutions)


def commonFactorSum(m, n):
    total = 0
    for a in range(1, m + 1):
        for b in range(1, n + 1):
            total += commonFactorLeastN(a, b)
    return total


def _g_small(a, b, searchLimit=1000):
    bestGcd = -1
    bestN = 0
    for n in range(searchLimit):
        value = math.gcd(n ** 3 + b, (n + a) ** 3 + b)
        if value > bestGcd:
            bestGcd = value
            bestN = n
    return bestN


def runTests():
    assert _g_small(1, 1) == 5
    assert commonFactorLeastN(1, 1) == 5
    assert commonFactorSum(5, 5) == 128_878
    assert commonFactorSum(10, 10) == 32_936_544


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = commonFactorSum(18, 1_900)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
