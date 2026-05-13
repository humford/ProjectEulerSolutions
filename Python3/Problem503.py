import fractions
import time


def expectedScoreExact(cards):
    continuation = fractions.Fraction(cards + 1, 2)

    for seen in range(cards - 2, -1, -1):
        scale = fractions.Fraction(cards + 1, seen + 2)
        stopCount = continuation // scale
        stopCount = min(stopCount, seen + 1)

        stopTotal = scale * stopCount * (stopCount + 1) / 2
        continueTotal = (seen + 1 - stopCount) * continuation
        continuation = (stopTotal + continueTotal) / (seen + 1)

    return continuation


def expectedScore(cards):
    continuation = (cards + 1) / 2

    for seen in range(cards - 2, -1, -1):
        scale = (cards + 1) / (seen + 2)
        stopCount = int(continuation / scale)
        stopCount = min(stopCount, seen + 1)

        stopTotal = scale * stopCount * (stopCount + 1) / 2
        continueTotal = (seen + 1 - stopCount) * continuation
        continuation = (stopTotal + continueTotal) / (seen + 1)

    return continuation


def roundedExpectedScore(cards, digits):
    return f"{expectedScore(cards):.{digits}f}"


def runTests():
    assert expectedScoreExact(3) == fractions.Fraction(5, 3)
    assert expectedScoreExact(4) == fractions.Fraction(15, 8)
    assert roundedExpectedScore(10, 10) == "2.5579365079"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedExpectedScore(10**6, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
