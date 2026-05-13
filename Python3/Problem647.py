import math
import time


def polygonalNumber(difference, index):
    return index * (difference * index + 2 - difference) // 2


def transformationPair(difference, multiplier):
    linearCoefficient = 1 + 2 * difference * multiplier
    offset = (2 - difference) * multiplier
    return linearCoefficient * linearCoefficient, polygonalNumber(difference, offset)


def transformationSumForDifference(difference, limit):
    total = 0
    multiplier = 1
    while True:
        coefficient, offset = transformationPair(difference, multiplier)
        if coefficient > limit or offset > limit:
            return total
        total += coefficient + offset
        multiplier += 1


def totalOddTransformationSum(limit):
    maxProduct = (math.isqrt(limit) - 1) // 2
    total = 0

    for difference in range(1, maxProduct + 1, 2):
        multiplier = 1
        while difference * multiplier <= maxProduct:
            coefficient, offset = transformationPair(difference, multiplier)
            if offset > limit:
                break
            total += coefficient + offset
            multiplier += 1

    return total


def polygonalTransformationSum(kind, limit):
    if kind == "all_odd":
        return totalOddTransformationSum(limit)
    if kind % 2 == 0 or kind < 3:
        raise ValueError("kind must be an odd polygonal parameter at least 3")

    difference = kind - 2
    return transformationSumForDifference(difference, limit)


def runTests():
    assert transformationPair(1, 1) == (9, 1)
    assert transformationPair(3, 1) == (49, 2)

    for difference in (1, 3, 5, 9):
        for multiplier in range(1, 5):
            coefficient, offset = transformationPair(difference, multiplier)
            linearCoefficient = 1 + 2 * difference * multiplier
            linearOffset = (2 - difference) * multiplier
            for index in range(1, 8):
                assert (
                    coefficient * polygonalNumber(difference, index) + offset
                    == polygonalNumber(
                        difference,
                        linearCoefficient * index + linearOffset,
                    )
                )

    assert polygonalTransformationSum(3, 100) == 184
    assert polygonalTransformationSum("all_odd", 10 ** 3) == 14_993


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = polygonalTransformationSum("all_odd", 10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
