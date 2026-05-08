import math
import time


def fractionCountBetweenOneThirdAndOneHalf(limit):
    count = 0

    for denominator in range(2, limit + 1):
        lower = denominator // 3 + 1
        upper = (denominator - 1) // 2

        for numerator in range(lower, upper + 1):
            if math.gcd(numerator, denominator) == 1:
                count += 1

    return count


def runTests():
    assert fractionCountBetweenOneThirdAndOneHalf(8) == 3


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fractionCountBetweenOneThirdAndOneHalf(12000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
