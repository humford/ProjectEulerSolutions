import functools
import math
import time


LOWER_BOUND = 2_000_000
UPPER_BOUND = 10 ** 9


def ceilSqrt(number):
    return math.isqrt(number - 1) + 1 if number > 0 else 0


def rayCountModerate(lowerBound, upperBound):
    total = 0

    for x in range(lowerBound + 1, upperBound + 1):
        xSquare = x * x
        maxQuotient = upperBound * upperBound // xSquare

        for quotient in range(1, maxQuotient + 1, 2):
            lowY = max(lowerBound + 1, ceilSqrt(quotient * xSquare))
            highY = min(upperBound, ceilSqrt((quotient + 1) * xSquare) - 1)

            if lowY <= highY:
                total += highY - lowY + 1

    return total


def normalizeQuadraticIrrational(integerPart, radicalCoefficient, denominator):
    common = math.gcd(math.gcd(abs(integerPart), radicalCoefficient), denominator)
    if common == 1:
        return integerPart, radicalCoefficient, denominator

    return (
        integerPart // common,
        radicalCoefficient // common,
        denominator // common,
    )


def floorQuadraticIrrational(integerPart, radicalCoefficient, denominator, radicand):
    return (integerPart + math.isqrt(radicalCoefficient * radicalCoefficient * radicand)) // denominator


@functools.cache
def floorSumQuadraticIrrational(
    count, integerPart, radicalCoefficient, denominator, radicand
):
    if count <= 0:
        return 0

    integerPart, radicalCoefficient, denominator = normalizeQuadraticIrrational(
        integerPart, radicalCoefficient, denominator
    )
    wholePart = floorQuadraticIrrational(
        integerPart, radicalCoefficient, denominator, radicand
    )

    if wholePart:
        return (
            wholePart * count * (count + 1) // 2
            + floorSumQuadraticIrrational(
                count,
                integerPart - wholePart * denominator,
                radicalCoefficient,
                denominator,
                radicand,
            )
        )

    finalValue = floorQuadraticIrrational(
        count * integerPart, count * radicalCoefficient, denominator, radicand
    )
    if finalValue == 0:
        return 0

    reciprocalDenominator = radicalCoefficient * radicalCoefficient * radicand - integerPart * integerPart
    return count * finalValue - floorSumQuadraticIrrational(
        finalValue,
        -integerPart * denominator,
        radicalCoefficient * denominator,
        reciprocalDenominator,
        radicand,
    )


@functools.cache
def floorRayBoundarySum(radicand, count):
    if count <= 0:
        return 0

    root = math.isqrt(radicand)
    if root * root == radicand:
        return root * count * (count + 1) // 2 - count

    return floorSumQuadraticIrrational(count, 0, 1, 1, radicand)


def floorRayBoundaryRangeSum(radicand, lower, upper):
    if upper < lower:
        return 0

    return floorRayBoundarySum(radicand, upper) - floorRayBoundarySum(
        radicand, lower - 1
    )


def rayCount(lowerBound=LOWER_BOUND, upperBound=UPPER_BOUND):
    total = 0
    upperSquare = upperBound * upperBound
    upperPlusOneSquare = (upperBound + 1) * (upperBound + 1)
    maxOddQuotient = upperSquare // ((lowerBound + 1) * (lowerBound + 1))
    if maxOddQuotient % 2 == 0:
        maxOddQuotient -= 1

    for quotient in range(1, maxOddQuotient + 1, 2):
        maxX = math.isqrt(upperSquare // quotient)
        if maxX <= lowerBound:
            continue

        uncappedUpperEnd = math.isqrt(upperPlusOneSquare // (quotient + 1))
        firstRangeEnd = min(maxX, uncappedUpperEnd)

        if firstRangeEnd > lowerBound:
            total += floorRayBoundaryRangeSum(
                quotient + 1, lowerBound + 1, firstRangeEnd
            )
            total -= floorRayBoundaryRangeSum(quotient, lowerBound + 1, firstRangeEnd)

        secondRangeStart = max(lowerBound + 1, firstRangeEnd + 1)
        if secondRangeStart <= maxX:
            total += (maxX - secondRangeStart + 1) * upperBound
            total -= floorRayBoundaryRangeSum(quotient, secondRangeStart, maxX)

    return total


def runTests():
    assert rayCountModerate(0, 100) == 3019
    assert rayCountModerate(100, 10000) == 29750422
    assert rayCount(0, 100) == 3019
    assert rayCount(100, 10000) == 29750422
    assert rayCount(5, 100) == rayCountModerate(5, 100)
    assert rayCount(200, 1000) == rayCountModerate(200, 1000)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rayCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
