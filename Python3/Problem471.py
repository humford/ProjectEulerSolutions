import functools
import time
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


PROBLEM_LIMIT = 10**11
HARMONIC_EXACT_LIMIT = 200_000
GAMMA_LIMIT = 200_000

getcontext().prec = 80
getcontext().rounding = ROUND_HALF_UP


def inradius(a, b):
    return Fraction(b * (a - 2 * b), a - b)


def exactTriangleSum(limit):
    total = Fraction(0, 1)
    for a in range(3, limit + 1):
        for b in range(1, (a - 1) // 2 + 1):
            total += inradius(a, b)
    return total


def harmonicDirect(limit):
    total = Decimal(0)
    for number in range(1, limit + 1):
        total += Decimal(1) / Decimal(number)
    return total


def harmonicCorrection(limit):
    n = Decimal(limit)
    inverse = Decimal(1) / n
    inverse2 = inverse * inverse
    inverse4 = inverse2 * inverse2
    inverse6 = inverse4 * inverse2
    inverse8 = inverse4 * inverse4
    inverse10 = inverse8 * inverse2

    return (
        inverse / 2
        - inverse2 / 12
        + inverse4 / 120
        - inverse6 / 252
        + inverse8 / 240
        - inverse10 / 132
    )


@functools.lru_cache(maxsize=None)
def eulerMascheroni():
    return (
        harmonicDirect(GAMMA_LIMIT)
        - Decimal(GAMMA_LIMIT).ln()
        - harmonicCorrection(GAMMA_LIMIT)
    )


@functools.lru_cache(maxsize=None)
def harmonic(limit):
    if limit <= 0:
        return Decimal(0)
    if limit <= HARMONIC_EXACT_LIMIT:
        return harmonicDirect(limit)
    return Decimal(limit).ln() + eulerMascheroni() + harmonicCorrection(limit)


def harmonicWeightedSums(limit, harmonicLimit):
    n = Decimal(limit)
    sum0 = (n + 1) * harmonicLimit - n
    sum1 = Decimal(limit * (limit + 1)) / 2 * harmonicLimit
    sum1 -= Decimal(limit * (limit - 1)) / 4
    sum2 = Decimal(limit * (limit + 1) * (2 * limit + 1)) / 6 * harmonicLimit
    sum2 -= Decimal(limit * (4 * limit**2 - 3 * limit - 1)) / 36
    return sum0, sum1, sum2


def triangularSum(limit):
    return limit * (limit + 1) // 2


def squareSum(limit):
    return limit * (limit + 1) * (2 * limit + 1) // 6


def ellipseTriangleSum(limit):
    if limit < 3:
        return Decimal(0)

    evenHalf = limit // 2
    oddHalf = (limit - 1) // 2

    polynomialPart = (
        3 * (squareSum(evenHalf) - triangularSum(evenHalf))
        + 3 * squareSum(oddHalf)
        + 2 * triangularSum(oddHalf)
    )

    upper = limit - 1
    harmonicUpper = harmonic(upper)
    sum0, sum1, sum2 = harmonicWeightedSums(upper, harmonicUpper)
    firstHarmonicPart = sum2 + 2 * sum1 + sum0 - 4

    if limit % 2 == 1:
        half = oddHalf
        harmonicHalf = harmonic(half)
        sum0, sum1, sum2 = harmonicWeightedSums(half, harmonicHalf)
        secondHarmonicPart = 8 * sum2 + 4 * sum1 + sum0 - 4
    else:
        half = evenHalf
        priorHalf = half - 1
        harmonicPrior = harmonic(priorHalf)
        sum0, sum1, sum2 = harmonicWeightedSums(priorHalf, harmonicPrior)
        secondHarmonicPart = 8 * sum2 + 4 * sum1 + sum0 - 4
        secondHarmonicPart += Decimal(4 * half**2) * harmonic(half)

    return Decimal(polynomialPart) - firstHarmonicPart + secondHarmonicPart


def formatFixedSignificant(value, digits):
    if value == 0:
        return "0"

    sign = "-" if value < 0 else ""
    value = abs(value)
    integerDigits = len(str(int(value))) if value >= 1 else 0
    decimalDigits = max(digits - integerDigits, 0)
    quantum = Decimal(1).scaleb(-decimalDigits)
    rounded = value.quantize(quantum)
    return sign + f"{rounded:.{decimalDigits}f}"


def formatScientific(value):
    if value == 0:
        return "0.000000000e0"

    sign = "-" if value < 0 else ""
    value = abs(value)
    exponent = value.adjusted()
    mantissa = value.scaleb(-exponent).quantize(Decimal("1.000000000"))

    if mantissa >= 10:
        mantissa = (mantissa / 10).quantize(Decimal("1.000000000"))
        exponent += 1

    return sign + f"{mantissa}e{exponent}"


def runTests():
    assert inradius(3, 1) == Fraction(1, 2)
    assert inradius(6, 2) == 1
    assert inradius(12, 3) == 2

    exact10 = exactTriangleSum(10)
    exact10Decimal = Decimal(exact10.numerator) / Decimal(exact10.denominator)
    assert formatFixedSignificant(exact10Decimal, 10) == "20.59722222"
    assert formatScientific(exact10Decimal) == "2.059722222e1"

    assert formatFixedSignificant(ellipseTriangleSum(10), 10) == "20.59722222"
    assert formatFixedSignificant(ellipseTriangleSum(100), 10) == "19223.60980"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formatScientific(ellipseTriangleSum(PROBLEM_LIMIT))
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
