from functools import lru_cache
from math import gcd
import time


def divisorsFromPrimePowers(factors):
    divisors = [1]

    for prime, exponent in factors.items():
        divisors = [
            divisor * primePower
            for divisor in divisors
            for primePower in (prime**e for e in range(exponent + 1))
        ]

    return divisors


def euclideanDepth(m, n):
    total = 0

    while n:
        quotient = m // n
        total += quotient
        m, n = n, m - quotient * n

    return total if m == 1 else None


@lru_cache(maxsize=None)
def rootValuesForPower(k):
    a = 6**k
    b = 10**k

    aDivisors = divisorsFromPrimePowers({2: k, 3: k})
    bDivisors = divisorsFromPrimePowers({2: k, 5: k})
    usefulDivisors = sorted(set(aDivisors + bDivisors))

    pairs = set()
    for m in usefulDivisors:
        for n in usefulDivisors:
            if gcd(m, n) == 1:
                pairs.add((m, n))

    for n in usefulDivisors:
        for divisorSum in usefulDivisors:
            m = divisorSum - n
            if m > 0 and gcd(m, n) == 1:
                pairs.add((m, n))

    values = {}

    for m, n in pairs:
        depth = euclideanDepth(m, n)
        if depth is None:
            continue

        x = m * (m + n)
        y = n * (m + n)
        z = m * n

        for alphaA, alphaB, alphaC in (
            (x, y, -z),
            (y, x, -z),
            (x, -z, y),
            (y, -z, x),
            (-z, x, y),
            (-z, y, x),
        ):
            numerator = -(alphaA * a + alphaB * b)
            if numerator % alphaC:
                continue

            c = numerator // alphaC
            if c <= 0:
                continue

            values[c] = min(values.get(c, depth), depth)

    return values


def fForPower(k, c):
    return rootValuesForPower(k).get(c, 0)


def FForPower(k):
    return sum(rootValuesForPower(k).values())


def solve():
    return sum(FForPower(k) for k in range(1, 19))


def runTests():
    assert fForPower(1, 35) == 3
    assert fForPower(1, 36) == 0
    assert FForPower(1) == 17
    assert FForPower(2) == 179


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
