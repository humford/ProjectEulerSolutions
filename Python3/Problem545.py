from functools import cache
from math import isqrt
import time


TARGET_DENOMINATOR = 20_010
BASE_MULTIPLE = 308
ALLOWED_PRIMES = {2, 3, 5, 23, 29}
BASE_DIVISORS = [
    divisor
    for divisor in range(1, BASE_MULTIPLE + 1)
    if BASE_MULTIPLE % divisor == 0
]


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * ((limit - start) // p + 1)
    return [p for p in range(limit + 1) if sieve[p]]


def isPrime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def divisors(n):
    result = [1]
    factor = 2
    remaining = n

    while factor * factor <= remaining:
        if remaining % factor == 0:
            power = 1
            newDivisors = []
            while remaining % factor == 0:
                remaining //= factor
                power *= factor
                newDivisors.extend(divisor * power for divisor in result)
            result.extend(newDivisors)
        factor += 1 if factor == 2 else 2

    if remaining > 1:
        result.extend(divisor * remaining for divisor in list(result))
    return result


def faulhaberDenominator(k):
    if k == 1:
        return 2
    if k % 2 == 1:
        return 1

    denominator = 1
    for divisor in divisors(k):
        prime = divisor + 1
        if isPrime(prime):
            denominator *= prime
    return denominator


@cache
def validMultipliers(limit):
    smallPrimes = primeSieve(isqrt(BASE_MULTIPLE * limit + 1))
    badMultiplier = bytearray(limit + 1)

    for factor in BASE_DIVISORS:
        possiblePrime = bytearray(b"\x01") * (limit + 1)
        possiblePrime[0] = 0

        for prime in smallPrimes:
            if factor % prime == 0:
                continue

            first = (-pow(factor % prime, -1, prime)) % prime
            if first == 0:
                first = prime
            possiblePrime[first : limit + 1 : prime] = b"\x00" * (
                (limit - first) // prime + 1
            )

            if (prime - 1) % factor == 0:
                multiplier = (prime - 1) // factor
                if 1 <= multiplier <= limit:
                    possiblePrime[multiplier] = 1

        for multiplier in range(1, limit + 1):
            if possiblePrime[multiplier] and factor * multiplier + 1 not in ALLOWED_PRIMES:
                badMultiplier[multiplier] = 1

    invalid = bytearray(limit + 1)
    for multiplier in range(1, limit + 1):
        if badMultiplier[multiplier] and not invalid[multiplier]:
            invalid[multiplier : limit + 1 : multiplier] = b"\x01" * (
                (limit - multiplier) // multiplier + 1
            )

    return [
        multiplier
        for multiplier in range(1, limit + 1)
        if not invalid[multiplier]
    ]


def faulhaberIndex(m):
    limit = max(1_000, 32 * m)

    while True:
        values = validMultipliers(limit)
        if len(values) >= m:
            return BASE_MULTIPLE * values[m - 1]
        limit *= 2


def runTests():
    assert faulhaberDenominator(4) == 30
    assert faulhaberDenominator(308) == TARGET_DENOMINATOR
    assert faulhaberIndex(1) == 308
    assert faulhaberIndex(10) == 96_404


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = faulhaberIndex(10 ** 5)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
