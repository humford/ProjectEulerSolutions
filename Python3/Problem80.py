import math
import time


def firstDigitsOfRoot(n, digit_count):
    return math.isqrt(n * 10 ** (2 * (digit_count - 1)))


def digitSum(n):
    return sum(int(digit) for digit in str(n))


def irrationalRootDigitalSum(limit, digit_count):
    total = 0

    for n in range(1, limit + 1):
        root = math.isqrt(n)
        if root * root != n:
            total += digitSum(firstDigitsOfRoot(n, digit_count))

    return total


def runTests():
    assert digitSum(firstDigitsOfRoot(2, 100)) == 475


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = irrationalRootDigitalSum(100, 100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
