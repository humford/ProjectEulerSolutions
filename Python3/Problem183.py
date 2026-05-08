import math
import time


def bestPartCount(number):
    lower = number // math.e
    candidates = [int(lower), int(lower) + 1]
    return max(candidates, key=lambda parts: parts * math.log(number / parts))


def terminatesInDecimal(numerator, denominator):
    divisor = math.gcd(numerator, denominator)
    denominator //= divisor

    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5

    return denominator == 1


def dValue(number):
    parts = bestPartCount(number)
    if terminatesInDecimal(number, parts):
        return -number
    return number


def dSum(limit):
    return sum(dValue(number) for number in range(5, limit + 1))


def runTests():
    assert dValue(8) == 8
    assert dValue(11) == -11


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = dSum(10000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
