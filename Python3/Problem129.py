import math
import time


def repunitDivisibilityLength(n):
    if math.gcd(n, 10) != 1:
        return 0

    remainder = 1 % n
    length = 1
    while remainder != 0:
        remainder = (remainder * 10 + 1) % n
        length += 1
    return length


def leastRepunitLengthAbove(threshold):
    n = threshold + 1

    while True:
        if math.gcd(n, 10) == 1 and repunitDivisibilityLength(n) > threshold:
            return n
        n += 1


def runTests():
    assert repunitDivisibilityLength(7) == 6
    assert repunitDivisibilityLength(41) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastRepunitLengthAbove(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
