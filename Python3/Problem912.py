from functools import lru_cache
import time


MODULUS = 1_000_000_007
TARGET_N = 10**16


def combineStats(left, right, shift):
    countLeft, oddLeft, sumLeft, squareLeft = left
    countRight, oddRight, sumRight, squareRight = right

    return (
        countLeft + countRight,
        oddLeft + oddRight,
        sumLeft + sumRight + shift * oddRight,
        squareLeft + squareRight + 2 * shift * sumRight + shift * shift * oddRight,
    )


@lru_cache(maxsize=None)
def completionStats(remainingBits, trailingOnes):
    if remainingBits == 0:
        isOdd = 1 if trailingOnes else 0
        return 1, isOdd, isOdd, isOdd

    zeroBlock = completionStats(remainingBits - 1, 0)
    if trailingOnes == 2:
        return zeroBlock

    oneBlock = completionStats(remainingBits - 1, trailingOnes + 1)
    return combineStats(zeroBlock, oneBlock, zeroBlock[0])


@lru_cache(maxsize=None)
def prefixStats(remainingBits, trailingOnes, prefixCount):
    if prefixCount == 0:
        return 0, 0, 0, 0

    fullStats = completionStats(remainingBits, trailingOnes)
    if prefixCount == fullStats[0]:
        return fullStats

    zeroBlock = completionStats(remainingBits - 1, 0)
    if prefixCount <= zeroBlock[0]:
        return prefixStats(remainingBits - 1, 0, prefixCount)

    onePrefix = prefixStats(
        remainingBits - 1,
        trailingOnes + 1,
        prefixCount - zeroBlock[0],
    )
    return combineStats(zeroBlock, onePrefix, zeroBlock[0])


def contribution(startOffset, blockStats):
    _, oddCount, positionSum, squareSum = blockStats
    return (
        oddCount * startOffset * startOffset
        + 2 * startOffset * positionSum
        + squareSum
    )


def F(limit):
    answer = 0
    offset = 0
    remaining = limit
    length = 1

    while remaining:
        blockStats = completionStats(length - 1, 1)
        count = blockStats[0]

        if remaining >= count:
            answer += contribution(offset, blockStats)
            offset += count
            remaining -= count
            length += 1
        else:
            partialStats = prefixStats(length - 1, 1, remaining)
            answer += contribution(offset, partialStats)
            break

    return answer % MODULUS


def hasNoTripleOnes(value):
    return "111" not in bin(value)


def bruteF(limit):
    validValues = []
    value = 1

    while len(validValues) < limit:
        if hasNoTripleOnes(value):
            validValues.append(value)
        value += 1

    return sum(
        index * index
        for index, value in enumerate(validValues, start=1)
        if value % 2 == 1
    )


def solve():
    return F(TARGET_N)


def runTests():
    assert F(10) == 199

    for limit in (1, 2, 7, 20, 100):
        assert F(limit) == bruteF(limit)

    assert solve() == 674_045_136


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
