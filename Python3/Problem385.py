import math
import time


LIMIT = 1_000_000_000
FOCUS_SUM = 39


def primitiveDirections():
    directions = []

    for norm in (1, 3, 13, 39):
        for first in range(-norm - 1, norm + 2):
            for second in range(-norm - 1, norm + 2):
                if (
                    math.gcd(first, second) == 1
                    and first * first + second * second - first * second == norm
                ):
                    directions.append((first, second, norm))

    return directions


def pellSeeds(discriminant):
    seeds = set()

    for yValue in range(1, 10 * discriminant + 100):
        xSquared = 3 * yValue * yValue + discriminant
        xValue = math.isqrt(xSquared)

        if xValue * xValue != xSquared:
            continue

        while True:
            previousX = 2 * xValue - 3 * yValue
            previousY = -xValue + 2 * yValue

            if previousX <= 0 or previousY <= 0:
                break

            xValue = previousX
            yValue = previousY

        seeds.add((xValue, yValue))

    return sorted(seeds)


def pellSolutions(discriminant, maxX, maxY):
    for xValue, yValue in pellSeeds(discriminant):
        while xValue <= maxX and yValue <= maxY:
            yield xValue, yValue
            xValue, yValue = 2 * xValue + 3 * yValue, xValue + 2 * yValue


def ellipseTriangleAreaSum(limit=LIMIT):
    rawAreaSum = 0

    for first, second, norm in primitiveDirections():
        discriminant = 3 * FOCUS_SUM // norm
        xCoefficients = [2 * first - second, -first + 2 * second, -first - second]
        yCoefficients = [second, -first, first - second]
        maxXCoefficient = max(abs(coefficient) for coefficient in xCoefficients)
        maxYCoefficient = max(abs(coefficient) for coefficient in yCoefficients)
        maxX = 3 * limit // maxXCoefficient
        maxY = limit // maxYCoefficient

        for xValue, yValue in pellSolutions(discriminant, maxX, maxY):
            if any((xValue * coefficient) % 3 != 0 for coefficient in xCoefficients):
                continue

            rawAreaSum += 2 * xValue * yValue * norm

    return rawAreaSum // 6


def runTests():
    assert ellipseTriangleAreaSum(8) == 72
    assert ellipseTriangleAreaSum(10) == 252
    assert ellipseTriangleAreaSum(100) == 34632
    assert ellipseTriangleAreaSum(1000) == 3529008


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = ellipseTriangleAreaSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
