from array import array
from math import isqrt
import time


def primesUpTo(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit // 2 + 1)
    sieve[0] = 0
    root = isqrt(limit)

    for prime in range(3, root + 1, 2):
        if sieve[prime // 2]:
            start = prime * prime // 2
            sieve[start::prime] = b"\x00" * (((len(sieve) - start - 1) // prime) + 1)

    primes = [2]
    primes.extend(2 * i + 1 for i in range(1, len(sieve)) if sieve[i])
    return primes


def buildDivisorPrefix(limit):
    smallestPrimeFactor = array("I", [0]) * (limit + 1)

    for n in range(2, limit + 1):
        if smallestPrimeFactor[n] == 0:
            smallestPrimeFactor[n] = n
            if n * n <= limit:
                for multiple in range(n * n, limit + 1, n):
                    if smallestPrimeFactor[multiple] == 0:
                        smallestPrimeFactor[multiple] = n

    divisorCounts = array("I", [0]) * (limit + 1)
    exponents = array("I", [0]) * (limit + 1)
    divisorCounts[1] = 1

    for n in range(2, limit + 1):
        prime = smallestPrimeFactor[n]
        rest = n // prime

        if rest % prime == 0:
            exponents[n] = exponents[rest] + 1
            divisorCounts[n] = divisorCounts[rest] // (exponents[rest] + 1) * (exponents[n] + 1)
        else:
            exponents[n] = 1
            divisorCounts[n] = divisorCounts[rest] * 2

    prefix = array("Q", [0]) * (limit + 1)
    total = 0
    for n in range(1, limit + 1):
        total += divisorCounts[n]
        prefix[n] = total

    return prefix


def buildSummatoryData(maxLimit):
    primes = primesUpTo(isqrt(maxLimit))
    primeSquares = [prime * prime for prime in primes]
    smallLimit = min(1_000_000, maxLimit)
    divisorPrefix = buildDivisorPrefix(smallLimit)
    return primes, primeSquares, divisorPrefix, smallLimit


def divisorSummatory(limit, prefix, smallLimit, cache):
    if limit <= smallLimit:
        return prefix[limit]
    if limit in cache:
        return cache[limit]

    root = isqrt(limit)
    total = 0
    start = 1

    while start <= root:
        quotient = limit // start
        end = min(limit // quotient, root)
        total += quotient * (end - start + 1)
        start = end + 1

    result = 2 * total - root * root
    cache[limit] = result
    return result


def replacementValue(number):
    if number == 1:
        return 1

    factors = 0
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            number //= divisor
            factors += 1
        divisor += 1 if divisor == 2 else 2

    if number > 1:
        factors += 1

    return 1 << factors


def replacementValueSum(limit, data=None):
    if data is None:
        data = buildSummatoryData(limit)

    primes, primeSquares, divisorPrefix, smallLimit = data
    divisorCache = {}
    total = 0

    def search(startIndex, currentNumber, currentWeight):
        nonlocal total

        total += currentWeight * divisorSummatory(limit // currentNumber, divisorPrefix, smallLimit, divisorCache)
        remaining = limit // currentNumber

        for i in range(startIndex, len(primes)):
            if primeSquares[i] > remaining:
                break

            prime = primes[i]
            primePower = primeSquares[i]
            weight = currentWeight

            while primePower <= remaining:
                search(i + 1, currentNumber * primePower, weight)
                primePower *= prime
                weight *= 2

    search(0, 1, 1)
    return total


def runTests(data):
    assert replacementValue(1) == 1
    assert replacementValue(90) == 16
    assert replacementValueSum(10 ** 8, data) == 9_613_563_919


if __name__ == "__main__":
    start = time.time()
    summatoryData = buildSummatoryData(10 ** 14)
    runTests(summatoryData)
    answer = replacementValueSum(10 ** 14, summatoryData)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
