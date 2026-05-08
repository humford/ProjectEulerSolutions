import math
import time


def pentagonalNumber(n):
    return n * (3 * n - 1) // 2


def testPentagonal(n):
    root = math.isqrt(24 * n + 1)
    return root * root == 24 * n + 1 and (root + 1) % 6 == 0


def pentagonalPairsWithDifference(difference):
    doubled = 2 * difference
    limit = math.isqrt(doubled)

    for factor in range(1, limit + 1):
        if doubled % factor != 0:
            continue

        gap_options = [factor]
        if factor != doubled // factor:
            gap_options.append(doubled // factor)

        for gap in gap_options:
            numerator = doubled // gap - 3 * gap + 1
            if numerator > 0 and numerator % 6 == 0:
                j = numerator // 6
                yield j, j + gap


def minimalPentagonalDifference():
    difference_index = 1
    while True:
        difference = pentagonalNumber(difference_index)
        for j, k in pentagonalPairsWithDifference(difference):
            if testPentagonal(pentagonalNumber(j) + pentagonalNumber(k)):
                return difference
        difference_index += 1


def runTests():
    assert pentagonalNumber(1) == 1
    assert pentagonalNumber(4) == 22
    assert pentagonalNumber(7) == 70
    assert pentagonalNumber(10) == 145
    assert testPentagonal(92)
    assert not testPentagonal(48)
    assert (1020, 2167) in list(pentagonalPairsWithDifference(5482660))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimalPentagonalDifference()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
