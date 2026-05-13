import functools
import math
import time


EULER_GAMMA = 0.57721566490153286060651209


@functools.cache
def binarySearchTotalComparisons(n):
    if n <= 0:
        return 0

    leftSize = (n - 1) // 2
    rightSize = n - 1 - leftSize
    return (
        n
        + binarySearchTotalComparisons(leftSize)
        + binarySearchTotalComparisons(rightSize)
    )


def binarySearchExpected(n):
    return binarySearchTotalComparisons(n) / n


def harmonicNumber(n):
    if n < 1_000_000:
        return sum(1 / value for value in range(1, n + 1))

    inverse = 1 / n
    inverseSquared = inverse * inverse
    return (
        math.log(n)
        + EULER_GAMMA
        + inverse / 2
        - inverseSquared / 12
        + inverseSquared * inverseSquared / 120
    )


def randomSearchExpected(n):
    return 2 * (n + 1) * harmonicNumber(n) / n - 3


def expectedDifference(n):
    return "{:.8f}".format(randomSearchExpected(n) - binarySearchExpected(n))


def runTests():
    assert "{:.8f}".format(binarySearchExpected(6)) == "2.33333333"
    assert "{:.8f}".format(randomSearchExpected(6)) == "2.71666667"
    assert expectedDifference(10 ** 3) == "2.99891266"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedDifference(10 ** 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
