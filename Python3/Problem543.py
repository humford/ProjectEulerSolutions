from functools import cache
from math import isqrt
import time


SMALL_PRIME_LIMIT = 1_000_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * ((limit - start) // p + 1)

    primes = []
    primeCounts = [0] * (limit + 1)
    count = 0
    for value in range(limit + 1):
        if sieve[value]:
            primes.append(value)
            count += 1
        primeCounts[value] = count
    return primes, primeCounts


PRIMES, SMALL_PRIME_COUNTS = primeSieve(SMALL_PRIME_LIMIT)


def integerRoot(n, exponent):
    if exponent == 2:
        return isqrt(n)

    root = int(n ** (1.0 / exponent))
    while (root + 1) ** exponent <= n:
        root += 1
    while root**exponent > n:
        root -= 1
    return root


@cache
def phi(x, primeCount):
    if primeCount == 0:
        return x
    return phi(x, primeCount - 1) - phi(x // PRIMES[primeCount - 1], primeCount - 1)


@cache
def primeCount(x):
    if x < len(SMALL_PRIME_COUNTS):
        return SMALL_PRIME_COUNTS[x]

    fourthRootCount = primeCount(integerRoot(x, 4))
    squareRootCount = primeCount(isqrt(x))
    cubeRootCount = primeCount(integerRoot(x, 3))

    total = (
        phi(x, fourthRootCount)
        + (squareRootCount + fourthRootCount - 2)
        * (squareRootCount - fourthRootCount + 1)
        // 2
    )

    for index in range(fourthRootCount + 1, squareRootCount + 1):
        quotient = x // PRIMES[index - 1]
        total -= primeCount(quotient)

        if index <= cubeRootCount:
            quotientRootCount = primeCount(isqrt(quotient))
            for secondIndex in range(index, quotientRootCount + 1):
                total -= primeCount(quotient // PRIMES[secondIndex - 1]) - (
                    secondIndex - 1
                )

    return total


def higherPrimeSumCount(n):
    highestK = n // 2
    if highestK < 3:
        return 0

    return (highestK - 2) * (n + 1) - (highestK * (highestK + 1) - 6)


def primeSumTotal(n):
    onePrime = primeCount(n)
    twoPrimes = max(0, n // 2 - 1)
    if n >= 5:
        twoPrimes += primeCount(n - 2) - 1

    return onePrime + twoPrimes + higherPrimeSumCount(n)


def fibonacciNumbers(limit):
    values = [0, 1]
    while len(values) <= limit:
        values.append(values[-1] + values[-2])
    return values


def fibonacciPrimeSumTotal():
    fibonacci = fibonacciNumbers(44)
    return sum(primeSumTotal(fibonacci[index]) for index in range(3, 45))


def runTests():
    assert primeSumTotal(10) == 20
    assert primeSumTotal(100) == 2_402
    assert primeSumTotal(1_000) == 248_838


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciPrimeSumTotal()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
