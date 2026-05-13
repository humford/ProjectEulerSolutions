from functools import lru_cache
import time


LIMIT = 1000


def maxWinningFirstMove(maxMove):
    @lru_cache(maxsize=None)
    def transform(blockSize, offset):
        if blockSize == 0:
            return tuple(
                position + offset if position + offset <= maxMove else 0
                for position in range(maxMove + 1)
            )

        lowerOffset = transform(blockSize - 1, offset)
        upperOffset = transform(blockSize - 1, offset + 1)
        return tuple(lowerOffset[position] for position in upperOffset)

    for blockSize in range(maxMove + 2):
        result = transform(blockSize, 0)

        if all(value == result[0] for value in result):
            return result[0]

    return transform(maxMove + 1, 0)[0]


def hoppingGameSum(limit=LIMIT):
    return sum(maxWinningFirstMove(maxMove) ** 3 for maxMove in range(1, limit + 1))


def runTests():
    assert maxWinningFirstMove(2) == 2
    assert maxWinningFirstMove(7) == 1
    assert maxWinningFirstMove(20) == 4
    assert hoppingGameSum(20) == 8150


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hoppingGameSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
