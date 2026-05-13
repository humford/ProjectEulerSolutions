import math
import time


P = 1_000_000_007


def containsDigitInBase(value, base, digit):
    if digit < 0 or digit >= base:
        return False

    while value:
        if value % base == digit:
            return True
        value //= base

    return digit == 0


def MBruteforce(base, digit):
    m = 1
    while True:
        if containsDigitInBase(m * m, base, digit):
            return m
        m += 1


def ceilSqrt(n):
    return math.isqrt(n - 1) + 1 if n > 0 else 0


def MForPrimeBaseDigitDifference(d, p=P):
    targetDigit = p - d
    legendreExponent = (p - 1) // 2
    sqrtExponent = (p + 1) // 4
    pSquared = p * p

    if pow(targetDigit, legendreExponent, p) == 1:
        root = pow(targetDigit, sqrtExponent, p)
        return min(root, p - root)

    lower = pSquared - d * p
    while True:
        m = ceilSqrt(lower)
        if m * m <= lower + p - 1:
            return m
        lower += pSquared


def solve(limit=100_000):
    total = 0
    for d in range(1, limit + 1):
        total += MForPrimeBaseDigitDifference(d)
    return total


def runTests():
    assert MBruteforce(10, 7) == 24
    assert MBruteforce(11, 10) == 19


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(100_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
