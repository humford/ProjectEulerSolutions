from decimal import Decimal, getcontext
import fractions
import time


def expectedOccupiedLine(limit):
    occupied = [fractions.Fraction(0) for _ in range(max(0, limit) + 1)]
    prefix = [fractions.Fraction(0) for _ in range(max(0, limit) + 1)]

    for seats in range(1, limit + 1):
        occupied[seats] = 1 + fractions.Fraction(2 * prefix[max(0, seats - 2)], seats)
        prefix[seats] = prefix[seats - 1] + occupied[seats]

    return occupied


def emptyChairExpectationSmall(seats):
    if seats <= 3:
        return fractions.Fraction(0)
    occupied = expectedOccupiedLine(seats - 3)
    expectedOccupied = 1 + occupied[seats - 3]
    return fractions.Fraction(seats, 1) - expectedOccupied


def emptyChairFractionSmall(seats):
    return emptyChairExpectationSmall(seats) / seats


def limitingEmptyFraction():
    getcontext().prec = 50
    return (Decimal(1) + Decimal(-2).exp()) / Decimal(2)


def emptyChairExpectation(seats):
    if seats <= 100:
        return emptyChairFractionSmall(seats)
    return format(limitingEmptyFraction(), ".14f")


def runTests():
    assert emptyChairExpectation(4) == fractions.Fraction(1, 2)
    assert emptyChairExpectation(6) == fractions.Fraction(5, 9)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = emptyChairExpectation(10 ** 18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
