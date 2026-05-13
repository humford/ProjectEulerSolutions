import time
from fractions import Fraction


def expectedSteps(n):
    if n <= 1:
        return 0.0

    expected = [0.0] * (n + 1)
    occupiedProbability = [0.0] * (n + 1)
    occupiedProbability[0] = 1.0
    inverseN = 1.0 / n

    for balls in range(1, n + 1):
        for occupied in range(balls, 0, -1):
            occupiedProbability[occupied] = (
                occupiedProbability[occupied] * occupied * inverseN
                + occupiedProbability[occupied - 1] * (n - occupied + 1) * inverseN
            )
        occupiedProbability[0] = 0.0

        if balls == 1:
            continue

        lowerExpectation = 0.0
        for occupied in range(1, balls):
            lowerExpectation += occupiedProbability[occupied] * expected[occupied]

        stayProbability = occupiedProbability[balls]
        expected[balls] = (1.0 + lowerExpectation) / (1.0 - stayProbability)

    return expected[n]


def expectedStepsExact(n):
    if n <= 1:
        return Fraction(0)

    expected = [Fraction(0) for _ in range(n + 1)]
    occupiedProbability = [Fraction(0) for _ in range(n + 1)]
    occupiedProbability[0] = Fraction(1)

    for balls in range(1, n + 1):
        nextProbability = [Fraction(0) for _ in range(n + 1)]
        for occupied in range(1, balls + 1):
            nextProbability[occupied] = (
                occupiedProbability[occupied] * Fraction(occupied, n)
                + occupiedProbability[occupied - 1] * Fraction(n - occupied + 1, n)
            )
        occupiedProbability = nextProbability

        if balls == 1:
            continue

        numerator = Fraction(1)
        for occupied in range(1, balls):
            numerator += occupiedProbability[occupied] * expected[occupied]

        expected[balls] = numerator / (1 - occupiedProbability[balls])

    return expected[n]


def formattedExpectedSteps(n):
    return f"{expectedSteps(n):.6f}"


def runTests():
    assert expectedStepsExact(3) == Fraction(27, 7)
    assert expectedStepsExact(5) == Fraction(468_125, 60_701)
    assert formattedExpectedSteps(5) == "7.711982"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedExpectedSteps(10 ** 3)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
