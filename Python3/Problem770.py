import math
import time
from fractions import Fraction


def reciprocalGuarantee(takes, gives):
    previous = [Fraction(1, 2 ** gives) for gives in range(gives + 1)]
    for takeCount in range(1, takes + 1):
        current = [Fraction(1, 1)]
        for giveCount in range(1, gives + 1):
            current.append((previous[giveCount] + current[giveCount - 1]) / 2)
        previous = current
    return previous[gives]


def centralBinomialRatioLog(n):
    value = float(n)
    inv = 1.0 / value
    inv2 = inv * inv
    inv3 = inv2 * inv
    inv5 = inv3 * inv2
    return (
        -0.5 * math.log(math.pi * value)
        - 0.125 * inv
        + inv3 / 192.0
        - inv5 / 640.0
    )


def centralRatioAtMost(n, numerator, denominator):
    return math.comb(2 * n, n) * denominator <= (1 << (2 * n)) * numerator


def gForFraction(numerator, denominator):
    if numerator <= 0 or denominator <= 0 or numerator >= 2 * denominator:
        raise ValueError("requires 0 < X < 2")

    ratioNumerator = 2 * denominator - numerator
    ratioDenominator = numerator
    common = math.gcd(ratioNumerator, ratioDenominator)
    ratioNumerator //= common
    ratioDenominator //= common

    ratio = ratioNumerator / ratioDenominator
    estimate = int(1.0 / (math.pi * ratio * ratio))
    if estimate < 20_000:
        n = 0
        while not centralRatioAtMost(n, ratioNumerator, ratioDenominator):
            n += 1
        return n

    logRatio = math.log(ratioNumerator) - math.log(ratioDenominator)
    n = max(1, estimate - 10)
    while centralBinomialRatioLog(n) > logRatio:
        n += 1
    while n > 1 and centralBinomialRatioLog(n - 1) <= logRatio:
        n -= 1
    return n


def runTests():
    assert reciprocalGuarantee(10, 10) <= Fraction(10, 17)
    assert Fraction(1, 1) / reciprocalGuarantee(10, 10) >= Fraction(17, 10)
    assert gForFraction(17, 10) == 10


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gForFraction(19_999, 10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
