import math
import time


def continuedFractionPeriod(n):
    root = math.isqrt(n)
    if root * root == n:
        return 0

    m = 0
    d = 1
    a = root
    period = 0

    while True:
        m = d * a - m
        d = (n - m * m) // d
        a = (root + m) // d
        period += 1

        if a == 2 * root:
            return period


def oddPeriodCount(limit):
    return sum(continuedFractionPeriod(n) % 2 == 1 for n in range(2, limit + 1))


def runTests():
    assert continuedFractionPeriod(2) == 1
    assert continuedFractionPeriod(3) == 2
    assert continuedFractionPeriod(13) == 5
    assert oddPeriodCount(13) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = oddPeriodCount(10000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
