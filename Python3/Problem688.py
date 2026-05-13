import time
from math import isqrt


MODULUS = 1_000_000_007
TARGET = 10 ** 16


def largestPossiblePileCount(plates):
    return (isqrt(8 * plates + 1) - 1) // 2


def smallestPileMaximum(plates, piles):
    offset = piles * (piles - 1) // 2
    if plates <= offset:
        return 0
    return (plates - offset) // piles


def pileFunction(plates):
    return sum(
        smallestPileMaximum(plates, piles)
        for piles in range(1, largestPossiblePileCount(plates) + 1)
    )


def pilePrefixSumExact(limit):
    maximumPiles = largestPossiblePileCount(limit)
    remaining = limit
    total = 0
    for piles in range(1, maximumPiles + 1):
        largestSmallestPile = remaining // piles
        total += (
            largestSmallestPile * (remaining + 1)
            - piles * largestSmallestPile * (largestSmallestPile + 1) // 2
        )
        remaining -= piles
    return total


def pilePrefixSum(limit, modulus=MODULUS):
    inverseTwo = (modulus + 1) // 2
    maximumPiles = largestPossiblePileCount(limit)
    remaining = limit
    remainingMod = limit % modulus
    total = 0

    for piles in range(1, maximumPiles + 1):
        largestSmallestPile = remaining // piles
        largestMod = largestSmallestPile % modulus

        firstTerm = largestMod * ((remainingMod + 1) % modulus) % modulus
        triangle = largestMod * ((largestMod + 1) % modulus) % modulus
        triangle = triangle * inverseTwo % modulus
        secondTerm = (piles % modulus) * triangle % modulus

        total += firstTerm - secondTerm
        total %= modulus

        remaining -= piles
        remainingMod -= piles
        remainingMod %= modulus

    return total


def bruteForcePilePrefixSum(limit):
    return sum(pileFunction(plates) for plates in range(1, limit + 1))


def runTests():
    assert smallestPileMaximum(10, 3) == 2
    assert smallestPileMaximum(10, 5) == 0
    assert pileFunction(100) == 275
    assert pilePrefixSumExact(100) == 12_656
    for limit in range(1, 101):
        assert pilePrefixSumExact(limit) == bruteForcePilePrefixSum(limit)
        assert pilePrefixSum(limit) == pilePrefixSumExact(limit) % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pilePrefixSum(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
