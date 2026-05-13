import time
from math import isqrt


LIMIT = 10**16
MODULUS = 7**10


def lowerWythoffIndex(number):
    return (isqrt(5 * number * number) - number) // 2


def floorSums(number):
    if number <= 0:
        return 0, 0, 0

    reduced = lowerWythoffIndex(number)
    reducedA, reducedB, reducedC = floorSums(reduced)
    sumIntegers = reduced * (reduced + 1) // 2
    sumSquares = reduced * (reduced + 1) * (2 * reduced + 1) // 6

    totalA = reduced * number - sumIntegers - reducedA

    thresholdSum = sumIntegers + reducedA + reduced
    thresholdSquareSum = (
        sumSquares
        + reducedC
        + reduced
        + 2 * reducedB
        + 2 * sumIntegers
        + 2 * reducedA
    )
    totalB = (
        reduced * number * (number + 1) // 2
        - (thresholdSquareSum - thresholdSum) // 2
    )

    weightedThresholdSum = sumSquares + reducedB + sumIntegers
    totalC = (number + 1) * reduced * reduced - (
        2 * weightedThresholdSum - thresholdSum
    )

    return totalA, totalB, totalC


def stoneGameSum(limit=LIMIT, modulus=MODULUS):
    split = lowerWythoffIndex(limit)
    sumA, sumB, sumC = floorSums(split)

    firstPart = 2 * sumB + (sumC + sumA) // 2
    secondPart = (
        (limit - split - 1) * (limit * (limit + 1) - split * (split + 1)) // 2
    )

    return (firstPart + secondPart) % modulus


def runTests():
    assert stoneGameSum(10, 10**18) == 211
    assert stoneGameSum(10**4, 10**18) == 230312207313


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = stoneGameSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
