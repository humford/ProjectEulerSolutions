from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction
from math import factorial
import time


def S(a, b):
    numerator = factorial(a) ** b * factorial(b) ** a
    denominator = factorial(a * b) ** 2
    return Fraction(numerator, denominator)


def formatScientific(value, digitsAfterDecimal=10):
    if value <= 0:
        raise ValueError("value must be positive")

    getcontext().prec = digitsAfterDecimal + 50
    decimalValue = Decimal(value.numerator) / Decimal(value.denominator)
    exponent = decimalValue.adjusted()
    mantissa = decimalValue.scaleb(-exponent)
    quantum = Decimal("1." + "0" * digitsAfterDecimal)
    mantissa = mantissa.quantize(quantum, rounding=ROUND_HALF_UP)

    if mantissa == Decimal(10):
        mantissa = Decimal(1).quantize(quantum)
        exponent += 1

    return f"{mantissa:.{digitsAfterDecimal}f}e{exponent}"


def runTests():
    assert S(2, 2) == Fraction(1, 36)
    assert S(2, 3) == Fraction(1, 1800)


def solve():
    return formatScientific(S(5, 8), 10)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
