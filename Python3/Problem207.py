import math
import time


def partitionCounts(limit):
    maximum_x = (1 + math.isqrt(1 + 4 * limit)) // 2
    total = max(0, maximum_x - 1)
    perfect = maximum_x.bit_length() - 1

    return perfect, total


def smallestPartitionLimitBelow(numerator, denominator):
    total = 0
    perfect = 0
    x = 1

    while True:
        x += 1
        total += 1
        if x & (x - 1) == 0:
            perfect += 1

        if perfect * denominator < total * numerator:
            return x * (x - 1)


def runTests():
    assert partitionCounts(6) == (1, 2)
    assert partitionCounts(185) == (3, 13)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smallestPartitionLimitBelow(1, 12345)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
