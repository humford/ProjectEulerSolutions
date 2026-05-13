import math
import time
from decimal import Decimal, ROUND_FLOOR, getcontext
from fractions import Fraction


getcontext().prec = 80

EULER_GAMMA = Decimal(
    "0.57721566490153286060651209008240243104215933593992"
)
LN10 = Decimal(10).ln()
LOG10_2 = Decimal(2).ln() / LN10


def gameAExpected(n):
    return sum(math.comb(n, k) / (k * 2 ** n) for k in range(1, n + 1))


def gameBExpected(n):
    return sum(1 / (k * math.comb(n, k)) for k in range(1, n + 1))


def harmonicNumberEstimate(n):
    value = Decimal(n)
    inverse = 1 / value
    inverse2 = inverse * inverse
    return (
        value.ln()
        + EULER_GAMMA
        + inverse / 2
        - inverse2 / 12
        + inverse2 * inverse2 / 120
        - inverse2 * inverse2 * inverse2 / 252
        + inverse2 ** 4 / 240
    )


def reciprocalDifference(n):
    return gameBExpected(n) - gameAExpected(n)


def reciprocalDifferenceExact(n):
    return sum(Fraction(1, k) for k in range(1, n + 1)) / (2 ** n)


def leadingDigitsOfDifference(n, digitCount=7):
    if n <= 200:
        difference = reciprocalDifferenceExact(n)
        while difference < 1:
            difference *= 10
        return (difference.numerator * 10 ** (digitCount - 1)) // difference.denominator

    harmonic = harmonicNumberEstimate(n)
    logarithm = harmonic.ln() / LN10 - Decimal(n) * LOG10_2
    integerPart = logarithm.to_integral_value(rounding=ROUND_FLOOR)
    fractionalPart = logarithm - integerPart
    scaled = ((fractionalPart + digitCount - 1) * LN10).exp()
    return int(scaled.to_integral_value(rounding=ROUND_FLOOR))


def runTests():
    assert "{:.8f}".format(gameAExpected(6)) == "0.39505208"
    assert "{:.8f}".format(gameBExpected(6)) == "0.43333333"
    assert "{:.8f}".format(reciprocalDifference(6)) == "0.03828125"
    assert leadingDigitsOfDifference(6) == 3_828_125
    assert leadingDigitsOfDifference(123_456_789) == 4_228_020


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leadingDigitsOfDifference(123_456_789)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
