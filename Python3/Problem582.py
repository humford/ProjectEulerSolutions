import time
from math import isqrt


MAX_DIFFERENCE = 100


def minimalPellSeeds(maxDifference=MAX_DIFFERENCE):
    seeds = []
    for difference in range(1, maxDifference + 1):
        for total in range(1, difference + 1):
            doubledHypotenuseSquared = 3 * total * total + difference * difference
            doubledHypotenuse = isqrt(doubledHypotenuseSquared)
            if doubledHypotenuse * doubledHypotenuse == doubledHypotenuseSquared:
                seeds.append((difference, total, doubledHypotenuse))
    return seeds


def nearlyIsoscelesCount(limit, maxDifference=MAX_DIFFERENCE):
    count = 0
    doubledLimit = 2 * limit

    for difference, total, doubledHypotenuse in minimalPellSeeds(maxDifference):
        while doubledHypotenuse <= doubledLimit:
            if total > difference and doubledHypotenuse % 2 == 0 and (total - difference) % 2 == 0:
                count += 1

            doubledHypotenuse, total = (
                2 * doubledHypotenuse + 3 * total,
                doubledHypotenuse + 2 * total,
            )

    return count


def bruteNearlyIsoscelesCount(limit, maxDifference=MAX_DIFFERENCE):
    count = 0
    for shortSide in range(1, limit + 1):
        longestOtherSide = min(shortSide + maxDifference, limit)
        for otherSide in range(shortSide, longestOtherSide + 1):
            hypotenuseSquared = shortSide * shortSide + shortSide * otherSide + otherSide * otherSide
            hypotenuse = isqrt(hypotenuseSquared)
            if hypotenuse * hypotenuse == hypotenuseSquared and hypotenuse <= limit:
                count += 1
    return count


def runTests():
    for limit in [50, 100, 1_000]:
        assert nearlyIsoscelesCount(limit) == bruteNearlyIsoscelesCount(limit)

    assert nearlyIsoscelesCount(1_000) == 235
    assert nearlyIsoscelesCount(10 ** 8) == 1_245


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nearlyIsoscelesCount(10 ** 100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
