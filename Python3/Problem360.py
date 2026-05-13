import time
from array import array
from math import isqrt


LIMIT = 10**10


def smallestPrimeFactorSieve(limit):
    factors = array("I", range(limit + 1))

    for number in range(2, isqrt(limit) + 1):
        if factors[number] != number:
            continue

        for multiple in range(number * number, limit + 1, number):
            if factors[multiple] == multiple:
                factors[multiple] = number

    return factors


def factor(number, smallestFactor):
    factors = {}

    while number > 1:
        prime = smallestFactor[number]
        exponent = 0

        while number % prime == 0:
            exponent += 1
            number //= prime

        factors[prime] = factors.get(prime, 0) + exponent

    return factors


def gaussianMultiply(first, second):
    real1, imag1 = first
    real2, imag2 = second

    return (
        real1 * real2 - imag1 * imag2,
        real1 * imag2 + imag1 * real2,
    )


def gaussianPower(value, exponent):
    result = (1, 0)
    base = value

    while exponent:
        if exponent & 1:
            result = gaussianMultiply(result, base)

        base = gaussianMultiply(base, base)
        exponent //= 2

    return result


def primeSquareRepresentation(prime, cache={}):
    if prime in cache:
        return cache[prime]

    for first in range(1, isqrt(prime) + 1):
        secondSquared = prime - first * first
        second = isqrt(secondSquared)

        if second * second == secondSquared:
            cache[prime] = (first, second)
            return cache[prime]

    raise ValueError("No two-square representation for " + str(prime))


def twoSquareRepresentations(factors):
    if not factors:
        return [(1, 0)]

    factors = dict(factors)
    representations = {(1, 0)}
    scale = 1
    twoExponent = factors.pop(2, 0)

    if twoExponent:
        scale *= 2 ** (twoExponent // 2)

        if twoExponent & 1:
            representations = {
                gaussianMultiply(representation, (1, 1))
                for representation in representations
            }

    for prime in list(factors):
        exponent = factors[prime]

        if prime % 4 != 3:
            continue

        if exponent & 1:
            return []

        scale *= prime ** (exponent // 2)
        del factors[prime]

    for prime, exponent in sorted(factors.items()):
        if prime % 4 != 1:
            continue

        first, second = primeSquareRepresentation(prime)
        primeFactors = [
            gaussianMultiply(
                gaussianPower((first, second), count),
                gaussianPower((first, -second), exponent - count),
            )
            for count in range(exponent + 1)
        ]
        representations = {
            gaussianMultiply(representation, primeFactor)
            for representation in representations
            for primeFactor in primeFactors
        }

    normalized = set()

    for first, second in representations:
        first = abs(first) * scale
        second = abs(second) * scale

        if first < second:
            first, second = second, first

        normalized.add((first, second))

    return normalized


def xyContribution(representations):
    count = 0
    total = 0

    for x, y in representations:
        if y == 0:
            count += 4
            total += 4 * x
        elif x == y:
            count += 4
            total += 8 * x
        else:
            count += 8
            total += 8 * (x + y)

    return count, total


def oddRadiusScarySphereSum(radius):
    smallestFactor = smallestPrimeFactorSieve(2 * radius)
    total = 0

    for z in range(radius + 1):
        if z == radius:
            pointCount = 1
            xySum = 0
        else:
            factors = factor(radius - z, smallestFactor)

            for prime, exponent in factor(radius + z, smallestFactor).items():
                factors[prime] = factors.get(prime, 0) + exponent

            pointCount, xySum = xyContribution(twoSquareRepresentations(factors))

        if z == 0:
            total += xySum
        else:
            total += 2 * (xySum + pointCount * z)

    return total


def scarySphereSum(radius=LIMIT):
    scale = 1

    while radius % 2 == 0:
        radius //= 2
        scale *= 2

    return scale * oddRadiusScarySphereSum(radius)


def scarySphereSumBrute(radius):
    total = 0
    square = radius * radius

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            zSquare = square - x * x - y * y

            if zSquare < 0:
                continue

            z = isqrt(zSquare)

            if z * z == zSquare:
                total += abs(x) + abs(y) + z

                if z != 0:
                    total += abs(x) + abs(y) + z

    return total


def runTests():
    assert scarySphereSum(1) == 6
    assert scarySphereSum(5) == 198
    assert scarySphereSum(45) == 34518
    assert scarySphereSum(45) == scarySphereSumBrute(45)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = scarySphereSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
