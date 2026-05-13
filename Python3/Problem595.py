import fractions
import math
import time


def successionCounts(size):
    counts = []
    for exact in range(size):
        count = 0
        for selected in range(exact, size):
            term = (
                math.comb(selected, exact)
                * math.comb(size - 1, selected)
                * math.factorial(size - selected)
            )
            if (selected - exact) % 2:
                count -= term
            else:
                count += term
        counts.append(count)

    return counts


def expectedShufflesAfterNextToss(n):
    expectations = [fractions.Fraction(0, 1)] * (n + 1)
    for size in range(2, n + 1):
        counts = successionCounts(size)
        totalPermutations = math.factorial(size)
        numerator = fractions.Fraction(1, 1)
        for successions in range(1, size):
            numerator += (
                fractions.Fraction(counts[successions], totalPermutations)
                * expectations[size - successions]
            )

        noMergeProbability = fractions.Fraction(counts[0], totalPermutations)
        expectations[size] = numerator / (1 - noMergeProbability)

    return expectations[n]


def expectedShuffles(n):
    if n == 1:
        return fractions.Fraction(0, 1)
    return expectedShufflesAfterNextToss(n) - 1


def formatExpectedShuffles(n):
    return f"{float(expectedShuffles(n)):.8f}"


def runTests():
    assert expectedShuffles(1) == 0
    assert expectedShuffles(2) == 1
    assert expectedShuffles(5) == fractions.Fraction(4213, 871)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formatExpectedShuffles(52)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
