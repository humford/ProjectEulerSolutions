import time
from decimal import Decimal, getcontext


def expectedSumSquare(n, k, precision=40):
    getcontext().prec = precision

    draws = Decimal(2 * k)
    kDecimal = Decimal(k)
    mean = Decimal(0)
    secondMoment = Decimal(0)
    population = Decimal(k * (n + 1))
    total = Decimal(0)

    for _ in range(n):
        afterAddMean = mean + kDecimal
        afterAddSecondMoment = secondMoment + 2 * kDecimal * mean + kDecimal * kDecimal

        denominator = population * (population - 1)
        c1 = draws * (population - draws) / denominator
        c2 = draws * (draws - 1) / denominator

        removedSecondMoment = c1 * afterAddMean + c2 * afterAddSecondMoment
        total += removedSecondMoment

        survivalRatio = (population - draws) / population
        mean = survivalRatio * afterAddMean

        secondMomentCoefficient = Decimal(1) - 2 * draws / population + c2
        secondMoment = (
            secondMomentCoefficient * afterAddSecondMoment
            + c1 * afterAddMean
        )

        population -= kDecimal

    return total


def roundedExpectedSumSquare(n, k):
    return int(expectedSumSquare(n, k) + Decimal("0.5"))


def runTests():
    assert abs(expectedSumSquare(2, 2) - Decimal("9.6")) < Decimal("1e-30")


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedExpectedSumSquare(10 ** 6, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
