import math
import time
from fractions import Fraction


def centralEulerian(n):
    total = 0
    exponent = 2 * n - 1

    for j in range(n):
        term = math.comb(2 * n, j) * (n - j) ** exponent
        if j % 2:
            total -= term
        else:
            total += term

    return total


def probabilityFraction(n):
    return Fraction(centralEulerian(n), math.factorial(2 * n - 1))


def roundedProbability(n, digits):
    numerator = centralEulerian(n)
    denominator = math.factorial(2 * n - 1)
    scale = 10 ** digits
    quotient, remainder = divmod(numerator * scale, denominator)

    if 2 * remainder >= denominator:
        quotient += 1

    integerPart = quotient // scale
    fractionalPart = quotient % scale
    return str(integerPart) + "." + str(fractionalPart).zfill(digits)


def runTests():
    assert probabilityFraction(3) == Fraction(11, 20)
    assert roundedProbability(5, 10) == "0.4304177690"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedProbability(80, 10)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
