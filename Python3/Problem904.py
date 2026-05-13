from fractions import Fraction
from math import acos, cos, degrees, floor, gcd, isqrt, radians, sqrt
import time


TARGET_N = 45_000
TARGET_L = 10_000_000_000


def angleFromLegRatio(ratio):
    square = ratio * ratio
    cosine = 2.0 * (1.0 + square) / sqrt((1.0 + 4.0 * square) * (4.0 + square))
    return degrees(acos(cosine))


def legRatioFromAngle(angle):
    cosineSquare = cos(radians(angle)) ** 2
    a = 4.0 * (cosineSquare - 1.0)
    b = 17.0 * cosineSquare - 8.0
    discriminant = b * b - 4.0 * a * a

    largeRoot = (-b - sqrt(discriminant)) / (2.0 * a)
    return sqrt(1.0 / largeRoot)


def euclidParametersFromRatio(ratio):
    root = sqrt(1.0 + ratio * ratio)
    return ratio / (1.0 + root), root - ratio


def compareFraction(numerator, denominator, targetNumerator, targetDenominator):
    left = numerator * targetDenominator
    right = targetNumerator * denominator
    return (left > right) - (left < right)


def fareyInterval(value, maxDenominator):
    target = Fraction.from_float(value)
    targetNumerator = target.numerator
    targetDenominator = target.denominator

    lowNumerator, lowDenominator = 0, 1
    highNumerator, highDenominator = 1, 1

    while lowDenominator + highDenominator <= maxDenominator:
        mediantNumerator = lowNumerator + highNumerator
        mediantDenominator = lowDenominator + highDenominator
        comparison = compareFraction(
            mediantNumerator,
            mediantDenominator,
            targetNumerator,
            targetDenominator,
        )

        if comparison == 0:
            return (
                (mediantNumerator, mediantDenominator),
                (mediantNumerator, mediantDenominator),
            )

        if comparison < 0:
            numeratorSlack = (
                targetNumerator * lowDenominator
                - lowNumerator * targetDenominator
            )
            denominatorSlack = (
                highNumerator * targetDenominator
                - targetNumerator * highDenominator
            )
            byDenominator = (maxDenominator - lowDenominator) // highDenominator
            byValue = (numeratorSlack - 1) // denominatorSlack
            multiple = max(1, min(byDenominator, byValue))
            lowNumerator += multiple * highNumerator
            lowDenominator += multiple * highDenominator
        else:
            numeratorSlack = (
                highNumerator * targetDenominator
                - targetNumerator * highDenominator
            )
            denominatorSlack = (
                targetNumerator * lowDenominator
                - lowNumerator * targetDenominator
            )
            byDenominator = (maxDenominator - highDenominator) // lowDenominator
            byValue = (numeratorSlack - 1) // denominatorSlack
            multiple = max(1, min(byDenominator, byValue))
            highNumerator += multiple * lowNumerator
            highDenominator += multiple * lowDenominator

    return (lowNumerator, lowDenominator), (highNumerator, highDenominator)


def previousFarey(fraction, successor, maxDenominator):
    numerator, denominator = fraction
    nextNumerator, nextDenominator = successor
    multiple = (maxDenominator + nextDenominator) // denominator
    return (
        multiple * numerator - nextNumerator,
        multiple * denominator - nextDenominator,
    )


def nextFarey(predecessor, fraction, maxDenominator):
    previousNumerator, previousDenominator = predecessor
    numerator, denominator = fraction
    multiple = (maxDenominator + previousDenominator) // denominator
    return (
        multiple * numerator - previousNumerator,
        multiple * denominator - previousDenominator,
    )


def primitiveTriangle(parameter):
    n, m = parameter
    if n <= 0 or n >= m or gcd(n, m) != 1:
        return None

    legA = m * m - n * n
    legB = 2 * m * n
    hypotenuse = m * m + n * n
    perimeter = 2 * m * (m + n)

    if (m + n) % 2 == 0:
        legA //= 2
        legB //= 2
        hypotenuse //= 2
        perimeter //= 2

    return legA, legB, hypotenuse, perimeter


def candidateFromParameter(parameter, limit):
    triangle = primitiveTriangle(parameter)
    if triangle is None:
        return None

    legA, legB, hypotenuse, perimeter = triangle
    if hypotenuse > limit:
        return None

    scale = limit // hypotenuse
    ratio = min(legA, legB) / max(legA, legB)
    angle = angleFromLegRatio(ratio)
    doubledArea = scale * scale * legA * legB

    return angle, scale * perimeter, doubledArea


def firstValidBelow(value, limit, maxDenominator):
    lower, upper = fareyInterval(value, maxDenominator)
    if lower == upper:
        candidate = candidateFromParameter(lower, limit)
        if candidate is not None:
            return candidate
        upper = nextFarey(lower, upper, maxDenominator)

    while lower[0] > 0:
        candidate = candidateFromParameter(lower, limit)
        if candidate is not None:
            return candidate
        previous = previousFarey(lower, upper, maxDenominator)
        upper = lower
        lower = previous

    return None


def firstValidAbove(value, limit, maxDenominator):
    lower, upper = fareyInterval(value, maxDenominator)
    if lower == upper:
        candidate = candidateFromParameter(upper, limit)
        if candidate is not None:
            return candidate
        lower = previousFarey(lower, upper, maxDenominator)

    while upper[0] < upper[1]:
        candidate = candidateFromParameter(upper, limit)
        if candidate is not None:
            return candidate
        following = nextFarey(lower, upper, maxDenominator)
        lower = upper
        upper = following

    return None


def f(angle, limit):
    ratio = legRatioFromAngle(angle)
    parameters = euclidParametersFromRatio(ratio)
    maxDenominator = isqrt(2 * limit)

    best = None
    for parameter in parameters:
        for candidate in (
            firstValidBelow(parameter, limit, maxDenominator),
            firstValidAbove(parameter, limit, maxDenominator),
        ):
            if candidate is None:
                continue
            candidateAngle, perimeter, doubledArea = candidate
            difference = abs(candidateAngle - angle)
            if best is None:
                best = (difference, doubledArea, perimeter)
            elif difference < best[0] - 1e-14:
                best = (difference, doubledArea, perimeter)
            elif abs(difference - best[0]) <= 1e-14 and doubledArea > best[1]:
                best = (difference, doubledArea, perimeter)

    return best[2]


def F(n, limit):
    return sum(f(index ** (1.0 / 3.0), limit) for index in range(1, n + 1))


def solve():
    return F(TARGET_N, TARGET_L)


def runTests():
    assert round(angleFromLegRatio(3 / 4), 12) == round(angleFromLegRatio(4 / 3), 12)
    assert f(30, 10**2) == 198
    assert f(10, 10**6) == 1_600_158
    assert F(10, 10**6) == 16_684_370
    assert solve() == 880_652_522_278_760


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
