from decimal import Decimal, getcontext
import math
import time


getcontext().prec = 80


def extendedGcd(a, b):
    oldRemainder, remainder = a, b
    oldS, s = 1, 0
    oldT, t = 0, 1
    while remainder:
        quotient = oldRemainder // remainder
        oldRemainder, remainder = (
            remainder,
            oldRemainder - quotient * remainder,
        )
        oldS, s = s, oldS - quotient * s
        oldT, t = t, oldT - quotient * t
    return oldS, oldT, oldRemainder


def ceilSqrt(n):
    if n <= 0:
        return 0
    root = math.isqrt(n)
    return root if root * root == n else root + 1


def determinantOnePoint(edgeX, edgeY):
    coefficientX, coefficientY, _ = extendedGcd(edgeX, edgeY)
    pointX = -coefficientY
    pointY = coefficientX

    lengthSquared = edgeX * edgeX + edgeY * edgeY
    projection = pointX * edgeX + pointY * edgeY
    if projection < 0:
        shift = (-projection + lengthSquared - 1) // lengthSquared
    else:
        shift = -(projection // lengthSquared)

    pointX += shift * edgeX
    pointY += shift * edgeY
    projection += shift * lengthSquared

    while projection < 0:
        pointX += edgeX
        pointY += edgeY
        projection += lengthSquared
    while projection >= lengthSquared:
        pointX -= edgeX
        pointY -= edgeY
        projection -= lengthSquared

    return pointX, pointY


def minimumParityNormSquared(edgeX, edgeY):
    return (edgeX & 1) + (edgeY & 1)


def feasibleTranslation(radius, edgeX, edgeY, pointX, pointY):
    fourRadiusSquared = 4 * radius * radius
    edgeLengthSquared = edgeX * edgeX + edgeY * edgeY
    slack = fourRadiusSquared - edgeLengthSquared
    limit = math.isqrt(slack)

    thirdOffsetX = -edgeX + 2 * pointX
    thirdOffsetY = -edgeY + 2 * pointY
    for midX in range(-limit, limit + 1):
        if (midX - edgeX) & 1:
            continue
        maxY = math.isqrt(slack - midX * midX)
        for midY in range(-maxY, maxY + 1):
            if (midY - edgeY) & 1:
                continue
            if (midX - edgeX) ** 2 + (midY - edgeY) ** 2 > fourRadiusSquared:
                continue
            if (midX + edgeX) ** 2 + (midY + edgeY) ** 2 > fourRadiusSquared:
                continue
            if (
                (midX + thirdOffsetX) ** 2
                + (midY + thirdOffsetY) ** 2
                > fourRadiusSquared
            ):
                continue
            return midX, midY
    return None


def decimalPerimeter(sideSquares):
    return sum(Decimal(value).sqrt() for value in sideSquares)


def perimeterUpperBound(radius, window):
    maxUnseenSquared = 4 * radius * radius - window
    if maxUnseenSquared <= 0:
        return Decimal(0)
    longest = Decimal(maxUnseenSquared).sqrt()
    return 2 * longest + Decimal(2) / longest


def annulusSearch(radius, window):
    maxLengthSquared = 4 * radius * radius
    minLengthSquared = max(0, maxLengthSquared - window)
    best = None

    for edgeX in range(0, 2 * radius + 1):
        remainingHigh = maxLengthSquared - edgeX * edgeX
        if remainingHigh < 0:
            break

        highY = math.isqrt(remainingHigh)
        lowY = ceilSqrt(minLengthSquared - edgeX * edgeX)
        if lowY > highY:
            continue

        for edgeY in range(lowY, highY + 1):
            if edgeX == 0 and edgeY == 0:
                continue

            edgeLengthSquared = edgeX * edgeX + edgeY * edgeY
            if edgeLengthSquared < minLengthSquared:
                continue
            if edgeLengthSquared > maxLengthSquared - minimumParityNormSquared(edgeX, edgeY):
                continue
            if math.gcd(edgeX, edgeY) != 1:
                continue

            pointX, pointY = determinantOnePoint(edgeX, edgeY)
            translation = feasibleTranslation(radius, edgeX, edgeY, pointX, pointY)
            if translation is None:
                continue

            sideSquares = (
                edgeLengthSquared,
                pointX * pointX + pointY * pointY,
                (pointX - edgeX) ** 2 + (pointY - edgeY) ** 2,
            )
            perimeter = decimalPerimeter(sideSquares)
            if best is None or perimeter > best["perimeter"]:
                best = {
                    "edge": (edgeX, edgeY),
                    "point": (pointX, pointY),
                    "translation": translation,
                    "sideSquares": sideSquares,
                    "perimeter": perimeter,
                }

    return best


def maximalTriangle(radius):
    window = min(max(128, 8_192), 4 * radius * radius)
    best = None

    while True:
        candidate = annulusSearch(radius, window)
        if candidate is not None and (
            best is None or candidate["perimeter"] > best["perimeter"]
        ):
            best = candidate

        if best is not None and best["perimeter"] > perimeterUpperBound(radius, window):
            return best

        if window >= 4 * radius * radius:
            if best is None:
                raise RuntimeError("No valid triangle found")
            return best
        window = min(window * 2, 4 * radius * radius)


def circumradiusSquaredNumerator(sideSquares):
    product = 1
    for value in sideSquares:
        product *= value
    return product


def roundedRatioFromSideSquares(sideSquares, radius):
    numerator = circumradiusSquaredNumerator(sideSquares)
    denominator = 2 * radius
    floorCandidate = math.isqrt(numerator) // denominator
    candidates = (floorCandidate, floorCandidate + 1)
    return min(
        candidates,
        key=lambda value: abs(numerator - (denominator * value) ** 2),
    )


def maximalPerimeterRatio(radius):
    triangle = maximalTriangle(radius)
    numerator = circumradiusSquaredNumerator(triangle["sideSquares"])
    return (Decimal(numerator).sqrt() / Decimal(2 * radius))


def roundedMaximalPerimeterRatio(radius):
    triangle = maximalTriangle(radius)
    return roundedRatioFromSideSquares(triangle["sideSquares"], radius)


def runTests():
    sample5 = maximalTriangle(5)
    assert sorted(sample5["sideSquares"]) == [13, 34, 89]
    assert format(maximalPerimeterRatio(10), ".5f") == "97.26729"
    assert format(maximalPerimeterRatio(100), ".5f") == "9157.64707"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedMaximalPerimeterRatio(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
