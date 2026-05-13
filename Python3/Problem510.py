import math
import time


def tangentCircleSum(limit):
    total = 0
    maxParameter = math.isqrt(math.isqrt(limit)) + 2

    for m in range(1, maxParameter + 1):
        for n in range(m, maxParameter + 1):
            if math.gcd(m, n) != 1:
                continue

            pairSum = m + n
            largestPrimitiveRadius = n * n * pairSum * pairSum
            if largestPrimitiveRadius > limit:
                break

            multiplierLimit = limit // largestPrimitiveRadius
            primitiveSum = pairSum * pairSum * (m * m + n * n) + m * m * n * n
            total += primitiveSum * multiplierLimit * (multiplierLimit + 1) // 2

    return total


def runTests():
    assert tangentCircleSum(5) == 9
    assert tangentCircleSum(100) == 3_072


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = tangentCircleSum(10**9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
