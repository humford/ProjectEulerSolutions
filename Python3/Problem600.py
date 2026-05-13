import math
import time


def tripleSumCount(limit):
    if limit < 3:
        return 0
    return math.comb(limit, 3)


def pairSumCount(limit):
    if limit < 2:
        return 0
    return math.comb(limit, 2)


def arithmeticSum(low, high):
    if high < low:
        return 0
    return (low + high) * (high - low + 1) // 2


def identityFixedCount(perimeter):
    total = tripleSumCount(perimeter // 2)
    for difference in range(1, perimeter // 3 + 1):
        total += 2 * tripleSumCount((perimeter - 3 * difference) // 2)
    return total


def rotationOneStepFixedCount(perimeter):
    return perimeter // 6


def rotationTwoStepFixedCount(perimeter):
    return pairSumCount(perimeter // 3)


def rotationThreeStepFixedCount(perimeter):
    return tripleSumCount(perimeter // 2)


def vertexReflectionFixedCount(perimeter):
    total = 0
    for middleSide in range(1, (perimeter - 3) // 3 + 1):
        maxFirstSide = (perimeter - 1 - 3 * middleSide) // 2
        if maxFirstSide < 1:
            continue

        splitFirstSide = min(
            maxFirstSide,
            (perimeter + 1 - 4 * middleSide) // 3,
        )
        if splitFirstSide >= 1:
            total += (
                arithmeticSum(1, splitFirstSide)
                + splitFirstSide * (middleSide - 1)
            )

        lowFirstSide = max(1, splitFirstSide + 1)
        if lowFirstSide <= maxFirstSide:
            count = maxFirstSide - lowFirstSide + 1
            total += (
                count * (perimeter - 3 * middleSide)
                - 2 * arithmeticSum(lowFirstSide, maxFirstSide)
            )

    return total


def edgeReflectionFixedCount(perimeter):
    halfPerimeter = perimeter // 2
    maxFirstSide = (halfPerimeter - 1) // 2
    return maxFirstSide * halfPerimeter - maxFirstSide * (maxFirstSide + 1)


def equiangularHexagons(perimeter):
    fixedSum = (
        identityFixedCount(perimeter)
        + 2 * rotationOneStepFixedCount(perimeter)
        + 2 * rotationTwoStepFixedCount(perimeter)
        + rotationThreeStepFixedCount(perimeter)
        + 3 * vertexReflectionFixedCount(perimeter)
        + 3 * edgeReflectionFixedCount(perimeter)
    )
    return fixedSum // 12


def runTests():
    assert equiangularHexagons(6) == 1
    assert equiangularHexagons(12) == 10
    assert equiangularHexagons(100) == 31_248


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = equiangularHexagons(55_106)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
