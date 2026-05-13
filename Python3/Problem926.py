from bisect import bisect_left
from collections import Counter
from math import isqrt
import time


MODULUS = 1_000_000_007
TARGET_N = 10_000_000


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, isqrt(limit) + 1):
        if isPrime[n]:
            isPrime[n * n:limit + 1:n] = b"\x00" * (((limit - n * n) // n) + 1)

    return [n for n in range(2, limit + 1) if isPrime[n]]


def exponentInFactorial(n, prime):
    exponent = 0

    while n:
        n //= prime
        exponent += n

    return exponent


def factorialPrimeExponentCounts(n):
    counts = Counter()

    for prime in primeSieve(n):
        counts[exponentInFactorial(n, prime)] += 1

    return counts


def totalRoundness(number):
    total = 0

    for base in range(2, number + 1):
        value = number
        while value % base == 0:
            total += 1
            value //= base

    return total


def factorialTotalRoundness(n):
    # A base b contributes one count for each k with b^k | n!.  Therefore
    # R(n!) = sum_k (number of nontrivial kth-power divisors of n!).
    counts = factorialPrimeExponentCounts(n)
    exponents = sorted(counts)
    answer = 0

    for k in range(1, exponents[-1] + 1):
        product = 1
        start = bisect_left(exponents, k)

        for exponent in exponents[start:]:
            product = (
                product
                * pow(exponent // k + 1, counts[exponent], MODULUS)
            ) % MODULUS

        answer = (answer + product - 1) % MODULUS

    return answer


def solve():
    return factorialTotalRoundness(TARGET_N)


def runTests():
    assert totalRoundness(20) == 6
    assert factorialTotalRoundness(10) == 312
    assert solve() == 40_410_219


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
