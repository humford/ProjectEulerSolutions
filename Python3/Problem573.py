import fractions
import math
import time


def winnerProbabilityExact(n, k):
    probability = fractions.Fraction(
        math.factorial(n - 1), math.factorial(k) * math.factorial(n - k)
    )
    probability *= fractions.Fraction(k, n) ** (k - 1)
    probability *= fractions.Fraction(n - k, n) ** (n - k)
    return probability


def expectedStartingNumberExact(n):
    return sum(k * winnerProbabilityExact(n, k) for k in range(1, n + 1))


def unfairRaceExpected(n):
    term = math.exp((n - 1) * math.log1p(-1 / n))
    total = term

    for k in range(1, n):
        remaining = n - k
        logRatio = k * math.log1p(1 / k)

        if remaining > 1:
            logRatio += (remaining - 1) * math.log1p(-1 / remaining)

        term *= math.exp(logRatio)
        total += term

    return total


def runTests():
    assert winnerProbabilityExact(3, 1) == fractions.Fraction(4, 9)
    assert winnerProbabilityExact(3, 2) == fractions.Fraction(2, 9)
    assert winnerProbabilityExact(3, 3) == fractions.Fraction(1, 3)
    assert expectedStartingNumberExact(3) == fractions.Fraction(17, 9)
    assert "{:.5f}".format(unfairRaceExpected(4)) == "2.21875"
    assert "{:.4f}".format(unfairRaceExpected(5)) == "2.5104"
    assert "{:.8f}".format(unfairRaceExpected(10)) == "3.66021568"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.4f}".format(unfairRaceExpected(1_000_000))
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
