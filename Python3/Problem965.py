from fractions import Fraction
import time


TARGET = 10_000


def fareyContributions(limit):
    a, b = 0, 1
    c, d = 1, limit

    while c <= limit:
        yield b, d
        k = (limit + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b


def exactF(limit):
    total = Fraction(0, 1)
    for leftDenominator, rightDenominator in fareyContributions(limit):
        total += Fraction(1, 2 * leftDenominator * rightDenominator**2)
    return total


def F(limit):
    total = 0.0
    correction = 0.0

    for leftDenominator, rightDenominator in fareyContributions(limit):
        term = 1.0 / (2.0 * leftDenominator * rightDenominator * rightDenominator)
        adjusted = term - correction
        newTotal = total + adjusted
        correction = (newTotal - total) - adjusted
        total = newTotal

    return total


def solve():
    return F(TARGET)


def runTests():
    assert exactF(1) == Fraction(1, 2)
    assert exactF(4) == Fraction(1, 4)
    assert exactF(10) == Fraction(19, 144)
    assert format(F(10), ".13f") == "0.1319444444444"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + format(answer, ".13f") + " in " + str(elapsed) + " seconds.")
