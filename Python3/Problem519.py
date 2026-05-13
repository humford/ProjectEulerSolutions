import math
import time


MODULUS = 10 ** 9


def tricolouredFountains(coins):
    if coins <= 0:
        return 0

    maxHeight = math.isqrt(2 * coins) + 2
    bufferSize = maxHeight + 3
    counts = [[0] * (maxHeight + 2) for _ in range(bufferSize)]
    counts[1 % bufferSize][1] = 3

    # Read a coloured fountain by successive frontier blocks.  If the current
    # frontier height is h, the next block can have any size 1 <= k <= h + 1.
    # The triangular 3-colouring forces all interior colours; only transitions
    # touching a height-1 frontier leave two choices instead of one.
    for usedCoins in range(1, coins):
        row = counts[usedCoins % bufferSize]
        maxUsedHeight = min(maxHeight, math.isqrt(2 * usedCoins) + 1)

        suffixSums = [0] * (maxUsedHeight + 3)
        runningTotal = 0
        for height in range(maxUsedHeight, 0, -1):
            runningTotal = (runningTotal + row[height]) % MODULUS
            suffixSums[height] = runningTotal

        remainingCoins = coins - usedCoins
        if runningTotal:
            counts[(usedCoins + 1) % bufferSize][1] += 2 * suffixSums[1]
            counts[(usedCoins + 1) % bufferSize][1] %= MODULUS

            if remainingCoins >= 2:
                counts[(usedCoins + 2) % bufferSize][2] += suffixSums[1] + row[1]
                counts[(usedCoins + 2) % bufferSize][2] %= MODULUS

            for nextHeight in range(3, min(maxHeight, maxUsedHeight + 1, remainingCoins) + 1):
                counts[(usedCoins + nextHeight) % bufferSize][nextHeight] += suffixSums[nextHeight - 1]
                counts[(usedCoins + nextHeight) % bufferSize][nextHeight] %= MODULUS

        for height in range(1, maxUsedHeight + 1):
            row[height] = 0

    finalRow = counts[coins % bufferSize]
    return sum(finalRow[1 : math.isqrt(2 * coins) + 1]) % MODULUS


def runTests():
    assert tricolouredFountains(4) == 48
    assert tricolouredFountains(10) == 17_760


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = tricolouredFountains(20_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
