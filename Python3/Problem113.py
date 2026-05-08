import math
import time


def nonBouncyBelowPowerOfTen(power):
    return math.comb(power + 10, 10) + math.comb(power + 9, 9) - 10 * power - 2


def runTests():
    assert nonBouncyBelowPowerOfTen(6) == 12951
    assert nonBouncyBelowPowerOfTen(10) == 277032


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nonBouncyBelowPowerOfTen(100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
