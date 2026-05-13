from fractions import Fraction
from functools import lru_cache
import time


def nextPowerTwoTimesThree(value):
    power = 1
    while 3 * power < value:
        power *= 2
    return 3 * power, power


@lru_cache(maxsize=None)
def p(m, n):
    if m == 1:
        return Fraction(1, 1)
    if n == 1:
        return Fraction(1, m)
    if n == 2:
        return Fraction(3, 2 * m)
    if m == 2:
        return Fraction(1, 1) - Fraction(1, 2 * n)
    if m == 3:
        return Fraction(1, 1) - Fraction(1, n)

    thresholdM, powerM = nextPowerTwoTimesThree(m)
    if powerM >= 2:
        lower = 3 * (powerM // 2)
        if n >= lower:
            return Fraction(1, 1) - Fraction(lower * (m - powerM), m * n)

    thresholdN, powerN = nextPowerTwoTimesThree(n)
    if n >= 3 and m >= thresholdN:
        return Fraction(thresholdN * (n - powerN), n * m)

    candidates = {1}
    half = m // 2
    for size in (half - 1, half, half + 1, (m + 1) // 2):
        if 1 < size < m:
            candidates.add(size)

    best = Fraction(-1, 1)
    for size in candidates:
        if size == 1:
            value = Fraction(1, m) + Fraction(m - 1, m) * (Fraction(1, 1) - p(n, m - 1))
        else:
            value = (
                Fraction(size, m) * (Fraction(1, 1) - p(n, size))
                + Fraction(m - size, m) * (Fraction(1, 1) - p(n, m - size))
            )
        best = max(best, value)

    return best


def roundFraction(value, digits):
    scale = 10**digits
    scaled = (value.numerator * scale * 2 + value.denominator) // (2 * value.denominator)
    return f"{scaled // scale}.{scaled % scale:0{digits}d}"


def solve():
    powers7 = [1]
    powers5 = [1]
    for _ in range(20):
        powers7.append(powers7[-1] * 7)
        powers5.append(powers5[-1] * 5)

    total = Fraction(0, 1)
    for m in powers7:
        for n in powers5:
            total += p(m, n)

    return roundFraction(total, 8)


def runTests():
    assert p(1, 10) == Fraction(1, 1)
    assert p(7, 1) == Fraction(1, 7)
    assert p(42, 1) == Fraction(1, 42)
    assert p(7, 5) == Fraction(18, 35)
    assert format(float(p(7, 5)), ".8f") == "0.51428571"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
