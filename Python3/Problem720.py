import time
from array import array


MODULUS = 1_000_000_007


def buildPermutationAndCodes(size):
    if size < 4 or size & (size - 1):
        raise ValueError("size must be a power of two at least 4")

    values = array("I", [1, 3, 2, 4])
    lehmerCodes = array("I", [0, 1, 0, 0])
    currentSize = 4

    while currentSize < size:
        halfSize = currentSize
        nextSize = currentSize * 2
        nextValues = array("I", [0]) * nextSize
        nextCodes = array("I", [0]) * nextSize

        for index in range(halfSize - 1):
            value = values[index]
            nextValues[index] = 2 * value - 1
            nextCodes[index] = value - 1 + lehmerCodes[index]

        nextValues[halfSize - 1] = 2
        nextCodes[halfSize - 1] = 0

        lastValue = values[halfSize - 1]
        nextValues[halfSize] = 2 * lastValue - 1
        nextCodes[halfSize] = halfSize - 2

        for index in range(1, halfSize):
            value = values[index]
            nextValues[halfSize + index] = 2 * value
            nextCodes[halfSize + index] = lehmerCodes[index]

        values = nextValues
        lehmerCodes = nextCodes
        currentSize = nextSize

    return values, lehmerCodes


def doubledRankFromPrevious(values, lehmerCodes, modulus=MODULUS):
    size = len(values)
    rank = 0
    factorial = 1
    factor = 1

    # Process the Lehmer code for the doubled permutation from right to left,
    # so the factorial multiplier can be grown without modular inverses.
    for index in range(size - 1, 0, -1):
        rank = (rank + lehmerCodes[index] * factorial) % modulus
        factorial = (factorial * factor) % modulus
        factor += 1

    rank = (rank + (size - 2) * factorial) % modulus
    factorial = (factorial * factor) % modulus
    factor += 1

    factorial = (factorial * factor) % modulus
    factor += 1

    for index in range(size - 2, -1, -1):
        code = values[index] - 1 + lehmerCodes[index]
        rank = (rank + code * factorial) % modulus
        factorial = (factorial * factor) % modulus
        factor += 1

    return rank


def firstUnpredictablePermutationPosition(size):
    if size < 1 or size & (size - 1):
        raise ValueError("size must be a power of two")
    if size <= 2:
        return 1
    if size == 4:
        return 3

    previousValues, previousCodes = buildPermutationAndCodes(size // 2)
    zeroBasedRank = doubledRankFromPrevious(previousValues, previousCodes)
    return (zeroBasedRank + 1) % MODULUS


def runTests():
    values4, _ = buildPermutationAndCodes(4)
    assert list(values4) == [1, 3, 2, 4]

    values8, _ = buildPermutationAndCodes(8)
    assert list(values8) == [1, 5, 3, 2, 7, 6, 4, 8]

    assert firstUnpredictablePermutationPosition(4) == 3
    assert firstUnpredictablePermutationPosition(8) == 2_295
    assert firstUnpredictablePermutationPosition(32) == 641_839_205


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstUnpredictablePermutationPosition(2**25)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
