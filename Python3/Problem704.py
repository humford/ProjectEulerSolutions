import math
import time


def twoAdicValuation(n):
    if n <= 0:
        raise ValueError("n must be positive")
    return (n & -n).bit_length() - 1


def v2Binomial(n, m):
    if m < 0 or m > n:
        raise ValueError("m must satisfy 0 <= m <= n")
    return m.bit_count() + (n - m).bit_count() - n.bit_count()


def maxV2Binomial(n):
    if n <= 0:
        raise ValueError("n must be positive")
    highestBit = n.bit_length() - 1
    return highestBit - min(twoAdicValuation(n + 1), highestBit)


def maxV2Prefix(limit):
    if limit <= 0:
        return 0

    highestBit = (limit + 1).bit_length() - 1
    logSum = (limit + 2) * highestBit - 2 * ((1 << highestBit) - 1)
    valuationSum = (limit + 1) - (limit + 1).bit_count()
    return logSum - valuationSum


def runTests():
    assert math.comb(12, 5) == 792
    assert v2Binomial(12, 5) == 3
    assert maxV2Binomial(10) == 3
    assert maxV2Binomial(100) == 6
    assert maxV2Prefix(100) == 389
    assert maxV2Prefix(10 ** 7) == 203_222_840


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maxV2Prefix(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
