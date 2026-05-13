from math import gcd
import sys
import time


MAX_FLIPS = 180


def stopValue(unfairProbability):
    if unfairProbability >= 0.5:
        return 70.0 * unfairProbability - 50.0
    return 20.0 - 70.0 * unfairProbability


def expectedCoinRoundValue(numerator, denominator, powersOfThree, inversePowersOfTwo):
    if numerator <= 0 or numerator >= denominator:
        return 20.0

    initialProbability = numerator / denominator
    initialOdds = initialProbability / (1.0 - initialProbability)
    nextRow = [0.0] * (MAX_FLIPS + 2)
    currentRow = [0.0] * (MAX_FLIPS + 2)

    base = initialOdds * inversePowersOfTwo[MAX_FLIPS]
    for heads in range(MAX_FLIPS + 1):
        odds = base * powersOfThree[heads]
        probability = odds / (1.0 + odds)
        nextRow[heads] = stopValue(probability)

    for flips in range(MAX_FLIPS - 1, -1, -1):
        base = initialOdds * inversePowersOfTwo[flips]
        for heads in range(flips + 1):
            odds = base * powersOfThree[heads]
            probability = odds / (1.0 + odds)
            stop = stopValue(probability)
            headProbability = 0.5 + 0.25 * probability
            keepGoing = -1.0 + headProbability * nextRow[heads + 1] + (1.0 - headProbability) * nextRow[heads]
            currentRow[heads] = max(stop, keepGoing)

        nextRow, currentRow = currentRow, nextRow

    return nextRow[0]


def precomputeRoundValues(maxCoins):
    powersOfThree = [1.0] * (MAX_FLIPS + 1)
    inversePowersOfTwo = [1.0] * (MAX_FLIPS + 1)
    for i in range(1, MAX_FLIPS + 1):
        powersOfThree[i] = powersOfThree[i - 1] * 3.0
        inversePowersOfTwo[i] = inversePowersOfTwo[i - 1] * 0.5

    neededFractions = set()
    for unfair in range(maxCoins + 1):
        for fair in range(maxCoins + 1):
            total = unfair + fair
            if total == 0:
                continue
            divisor = gcd(unfair, total)
            neededFractions.add((unfair // divisor, total // divisor))

    return {
        fraction: expectedCoinRoundValue(fraction[0], fraction[1], powersOfThree, inversePowersOfTwo)
        for fraction in neededFractions
    }


def S(coins):
    roundValues = precomputeRoundValues(coins)
    dp = [[0.0] * (coins + 1) for _ in range(coins + 1)]

    for total in range(1, 2 * coins + 1):
        minUnfair = max(0, total - coins)
        maxUnfair = min(coins, total)

        for unfair in range(minUnfair, maxUnfair + 1):
            fair = total - unfair
            divisor = gcd(unfair, total)
            immediate = roundValues[(unfair // divisor, total // divisor)]
            expectedFuture = 0.0
            if unfair:
                expectedFuture += (unfair / total) * dp[unfair - 1][fair]
            if fair:
                expectedFuture += (fair / total) * dp[unfair][fair - 1]
            dp[unfair][fair] = immediate + expectedFuture

    return dp[coins][coins]


def runTests():
    assert format(S(1), ".6f") == "20.558591"


def solve(coins=50):
    return format(S(coins), ".6f")


if __name__ == "__main__":
    runTests()
    n = 50
    if len(sys.argv) >= 2:
        n = int(sys.argv[1])

    start = time.time()
    answer = solve(n)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
