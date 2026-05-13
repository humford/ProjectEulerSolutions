from functools import cache
from math import isqrt
import time


MODULUS = 10 ** 9


def sqrtFloorSum(limit):
    if limit <= 0:
        return 0

    root = isqrt(limit)
    return (
        (root - 1) * root * (4 * root + 1) // 6
        + root * (limit - root * root + 1)
    )


@cache
def rootPrefixSum(position):
    if position == 0:
        return 0

    copiedCount = copiedElementsThrough(position)
    circledCount = position - copiedCount
    return rootPrefixSum(copiedCount) + sqrtFloorSum(circledCount)


@cache
def copiedElementsThrough(position):
    if position <= 1:
        return 0

    low = 0
    high = position - 1
    while low < high:
        middle = (low + high + 1) // 2
        if middle + rootPrefixSum(middle) <= position:
            low = middle
        else:
            high = middle - 1
    return low


@cache
def fractalSequenceSum(position):
    if position == 0:
        return 0

    copiedCount = copiedElementsThrough(position)
    circledCount = position - copiedCount
    return fractalSequenceSum(copiedCount) + circledCount * (circledCount + 1) // 2


def runTests():
    assert sqrtFloorSum(20) == sum(isqrt(i) for i in range(1, 21))
    assert fractalSequenceSum(1) == 1
    assert fractalSequenceSum(20) == 86
    assert fractalSequenceSum(10 ** 3) == 364_089
    assert fractalSequenceSum(10 ** 9) == 498_676_527_978_348_241


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fractalSequenceSum(10 ** 18) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
