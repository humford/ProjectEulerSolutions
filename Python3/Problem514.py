import itertools
import math
import time

import numpy


def polygonDoubleArea(points):
    total = 0
    for i, point in enumerate(points):
        nextPoint = points[(i + 1) % len(points)]
        total += point[0] * nextPoint[1] - point[1] * nextPoint[0]
    return abs(total)


def convexHull(points):
    points = sorted(points)
    if len(points) <= 1:
        return points

    def cross(origin, first, second):
        return (
            (first[0] - origin[0]) * (second[1] - origin[1])
            - (first[1] - origin[1]) * (second[0] - origin[0])
        )

    lower = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)

    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)

    return lower[:-1] + upper[:-1]


def bruteExpectedGeoboardArea(order):
    points = list(itertools.product(range(order + 1), repeat=2))
    pinProbability = 1.0 / (order + 1)
    missProbability = 1.0 - pinProbability
    total = 0.0

    for mask in range(1 << len(points)):
        selected = [points[i] for i in range(len(points)) if mask & (1 << i)]
        probability = pinProbability ** len(selected) * missProbability ** (len(points) - len(selected))
        if len(selected) < 3:
            continue

        hull = convexHull(selected)
        if len(hull) >= 3:
            total += probability * polygonDoubleArea(hull) / 2.0

    return total


def _rectangleSum(prefixSums, xMin, xMax, yMin, yMax):
    total = prefixSums[xMax, yMax]
    if xMin:
        total -= prefixSums[xMin - 1, yMax]
    if yMin:
        total -= prefixSums[xMax, yMin - 1]
    if xMin and yMin:
        total += prefixSums[xMin - 1, yMin - 1]
    return float(total)


def expectedGeoboardAreaValue(order):
    pinProbability = 1.0 / (order + 1)
    missProbability = 1.0 - pinProbability
    coordinates = numpy.arange(order + 1, dtype=numpy.int64)
    xCoordinates, yCoordinates = numpy.meshgrid(coordinates, coordinates, indexing="ij")
    totalShoelace = 0.0

    # A directed pair P -> Q is an edge in the boundary walk exactly when both
    # endpoints are pinned, no pinned point lies strictly to its right, and no
    # pinned point lies on the open segment.  The expected shoelace sum can
    # therefore be accumulated over all directed pairs.
    for xDirection in range(-order, order + 1):
        for yDirection in range(-order, order + 1):
            if xDirection == 0 and yDirection == 0:
                continue
            if math.gcd(abs(xDirection), abs(yDirection)) != 1:
                continue

            maxMultiplier = order
            if xDirection:
                maxMultiplier = min(maxMultiplier, order // abs(xDirection))
            if yDirection:
                maxMultiplier = min(maxMultiplier, order // abs(yDirection))

            lineValues = xCoordinates * yDirection - yCoordinates * xDirection
            distinctValues, valueCounts = numpy.unique(lineValues, return_counts=True)
            rightCounts = (order + 1) * (order + 1) - numpy.cumsum(valueCounts)
            powersByLineValue = numpy.zeros(distinctValues[-1] - distinctValues[0] + 1, dtype=numpy.float64)
            powersByLineValue[distinctValues - distinctValues[0]] = numpy.power(missProbability, rightCounts)

            weights = lineValues.astype(numpy.float64) * powersByLineValue[lineValues - distinctValues[0]]
            prefixSums = weights.cumsum(axis=0).cumsum(axis=1)

            segmentProbability = 1.0
            for multiplier in range(1, maxMultiplier + 1):
                xDelta = multiplier * xDirection
                yDelta = multiplier * yDirection
                xMin = max(0, -xDelta)
                xMax = min(order, order - xDelta)
                yMin = max(0, -yDelta)
                yMax = min(order, order - yDelta)

                if xMin <= xMax and yMin <= yMax:
                    totalShoelace += multiplier * segmentProbability * _rectangleSum(
                        prefixSums, xMin, xMax, yMin, yMax
                    )
                segmentProbability *= missProbability

    return 0.5 * pinProbability * pinProbability * totalShoelace


def expectedGeoboardArea(order):
    return "{:.5f}".format(expectedGeoboardAreaValue(order))


def runTests():
    assert "{:.5f}".format(bruteExpectedGeoboardArea(1)) == "0.18750"
    assert "{:.5f}".format(bruteExpectedGeoboardArea(2)) == "0.94335"
    assert expectedGeoboardArea(1) == "0.18750"
    assert expectedGeoboardArea(2) == "0.94335"
    assert expectedGeoboardArea(10) == "55.03013"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedGeoboardArea(100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
