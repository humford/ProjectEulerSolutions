import time
from fractions import Fraction


def maximumProductFloor(m):
    product = Fraction(1, 1)

    for i in range(1, m + 1):
        product *= Fraction(2 * i, m + 1) ** i

    return product.numerator // product.denominator


def maximumProductFloorSum(limit):
    return sum(maximumProductFloor(m) for m in range(2, limit + 1))


def runTests():
    assert maximumProductFloor(2) == 1


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumProductFloorSum(15)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
