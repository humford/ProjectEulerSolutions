import math
import time


def minimalPellSolution(D):
    root = math.isqrt(D)
    if root * root == D:
        return None

    m = 0
    d = 1
    a = root

    numerator_previous = 1
    numerator = a
    denominator_previous = 0
    denominator = 1

    while numerator * numerator - D * denominator * denominator != 1:
        m = d * a - m
        d = (D - m * m) // d
        a = (root + m) // d

        numerator_previous, numerator = (
            numerator,
            a * numerator + numerator_previous,
        )
        denominator_previous, denominator = (
            denominator,
            a * denominator + denominator_previous,
        )

    return numerator, denominator


def largestMinimalX(limit):
    best_D = None
    best_x = 0

    for D in range(2, limit + 1):
        solution = minimalPellSolution(D)
        if solution is None:
            continue

        x, _ = solution
        if x > best_x:
            best_x = x
            best_D = D

    return best_D


def runTests():
    assert minimalPellSolution(2) == (3, 2)
    assert minimalPellSolution(5) == (9, 4)
    assert minimalPellSolution(13) == (649, 180)
    assert largestMinimalX(7) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestMinimalX(1000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
