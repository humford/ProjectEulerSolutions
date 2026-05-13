import time
from collections import defaultdict
from math import gcd, isqrt


def buildPythagoreanLegMaps(limit):
    halfLimit = limit // 2
    maxHalfWidth = (halfLimit - 1) // 2
    maxLeg = halfLimit

    longDiagonalLegs = defaultdict(list)
    rectangleHeights = defaultdict(list)
    maxM = isqrt(2 * maxLeg) + 2

    for m in range(2, maxM + 1):
        mSquared = m * m
        for n in range(1 + (m & 1), m, 2):
            if gcd(m, n) != 1:
                continue

            legA = mSquared - n * n
            legB = 2 * m * n
            if legA > maxLeg and legB > maxLeg:
                continue

            multiplier = 1
            while True:
                scaledA = legA * multiplier
                scaledB = legB * multiplier
                if scaledA > maxLeg and scaledB > maxLeg:
                    break

                if scaledA <= maxHalfWidth and scaledB <= maxLeg:
                    longDiagonalLegs[scaledA].append(scaledB)
                if scaledB <= maxHalfWidth and scaledA <= maxLeg:
                    longDiagonalLegs[scaledB].append(scaledA)

                if scaledA <= 2 * maxHalfWidth and scaledA % 2 == 0 and scaledB <= maxLeg:
                    rectangleHeights[scaledA // 2].append(scaledB)
                if scaledB <= 2 * maxHalfWidth and scaledB % 2 == 0 and scaledA <= maxLeg:
                    rectangleHeights[scaledB // 2].append(scaledA)

                multiplier += 1

    return longDiagonalLegs, {
        halfWidth: set(heights)
        for halfWidth, heights in rectangleHeights.items()
    }


def heronEnvelopePerimeterSum(limit):
    halfLimit = limit // 2
    maxHalfWidth = (halfLimit - 1) // 2
    longDiagonalLegs, rectangleHeights = buildPythagoreanLegMaps(limit)

    perimeterSum = 0
    maxM = isqrt(2 * halfLimit) + 2

    for m in range(2, maxM + 1):
        mSquared = m * m
        for n in range(1 + (m & 1), m, 2):
            if gcd(m, n) != 1:
                continue

            legA = mSquared - n * n
            legB = 2 * m * n
            hypotenuse = mSquared + n * n
            multiplier = 1

            while multiplier * (legA + legB + hypotenuse) < halfLimit:
                scaledA = legA * multiplier
                scaledB = legB * multiplier
                flapSide = hypotenuse * multiplier

                for halfWidth, flapHeight in ((scaledA, scaledB), (scaledB, scaledA)):
                    if halfWidth > maxHalfWidth or halfWidth + flapSide + flapHeight >= halfLimit:
                        continue

                    possibleRectangleHeights = rectangleHeights.get(halfWidth)
                    possibleLongHeights = longDiagonalLegs.get(halfWidth)
                    if not possibleRectangleHeights or not possibleLongHeights:
                        continue

                    maxRectangleHeight = halfLimit - halfWidth - flapSide
                    for totalHeight in possibleLongHeights:
                        rectangleHeight = totalHeight - flapHeight
                        if (
                            rectangleHeight > flapHeight
                            and rectangleHeight <= maxRectangleHeight
                            and rectangleHeight in possibleRectangleHeights
                        ):
                            perimeterSum += 2 * (rectangleHeight + flapSide + halfWidth)

                multiplier += 1

    return perimeterSum


def bruteHeronEnvelopePerimeterSum(limit):
    perimeterSum = 0
    halfLimit = limit // 2
    for halfWidth in range(1, halfLimit):
        for flapHeight in range(1, halfLimit):
            flapSideSquared = halfWidth * halfWidth + flapHeight * flapHeight
            flapSide = isqrt(flapSideSquared)
            if flapSide * flapSide != flapSideSquared:
                continue

            maxRectangleHeight = halfLimit - halfWidth - flapSide
            for rectangleHeight in range(flapHeight + 1, maxRectangleHeight + 1):
                rectangleDiagonalSquared = (2 * halfWidth) ** 2 + rectangleHeight * rectangleHeight
                rectangleDiagonal = isqrt(rectangleDiagonalSquared)
                if rectangleDiagonal * rectangleDiagonal != rectangleDiagonalSquared:
                    continue

                longDiagonalSquared = halfWidth * halfWidth + (rectangleHeight + flapHeight) ** 2
                longDiagonal = isqrt(longDiagonalSquared)
                if longDiagonal * longDiagonal == longDiagonalSquared:
                    perimeterSum += 2 * (rectangleHeight + flapSide + halfWidth)

    return perimeterSum


def runTests():
    for limit in [200, 500]:
        assert heronEnvelopePerimeterSum(limit) == bruteHeronEnvelopePerimeterSum(limit)

    assert heronEnvelopePerimeterSum(10 ** 4) == 884_680


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = heronEnvelopePerimeterSum(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
