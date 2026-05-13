import bisect
from functools import lru_cache
import itertools
import math
import time


LIMIT = 10**8


def primeList(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit // 2)
    sieve[0] = 0

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number // 2]:
            start = number * number // 2
            step = number
            sieve[start::step] = b"\x00" * (((len(sieve) - 1 - start) // step) + 1)

    return [2] + [
        2 * index + 1
        for index, isPrime in enumerate(sieve)
        if isPrime and 2 * index + 1 <= limit
    ]


def factorExponents(number):
    exponents = []
    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            exponent = 0

            while number % divisor == 0:
                number //= divisor
                exponent += 1

            exponents.append(exponent)

        divisor += 1 if divisor == 2 else 2

    if number > 1:
        exponents.append(1)

    return exponents


def maximumAntichainLengthFromExponents(exponents):
    coefficients = [1]

    for exponent in exponents:
        nextCoefficients = [0] * (len(coefficients) + exponent)

        for index, value in enumerate(coefficients):
            for add in range(exponent + 1):
                nextCoefficients[index + add] += value

        coefficients = nextCoefficients

    return max(coefficients)


def maximumAntichainLength(number):
    return maximumAntichainLengthFromExponents(factorExponents(number))


def exponentPatterns(limit, primes):
    patterns = []
    maxExponent = 0
    power = 1

    while power * 2 <= limit:
        power *= 2
        maxExponent += 1

    def search(previousExponent, primeIndex, product, pattern):
        for exponent in range(previousExponent, 0, -1):
            nextProduct = product * (primes[primeIndex] ** exponent)

            if nextProduct > limit:
                continue

            nextPattern = pattern + (exponent,)
            patterns.append(nextPattern)
            search(exponent, primeIndex + 1, nextProduct, nextPattern)

    search(maxExponent, 0, 1, ())
    return patterns


def integerRoot(number, exponent):
    if exponent == 1:
        return number

    low = 1
    high = int(number ** (1.0 / exponent)) + 3

    while high**exponent <= number:
        high *= 2

    while low + 1 < high:
        middle = (low + high) // 2

        if middle**exponent <= number:
            low = middle
        else:
            high = middle

    return low


def maximumAntichainSum(limit=LIMIT):
    primes = primeList(limit)
    patterns = exponentPatterns(limit, primes)

    @lru_cache(maxsize=None)
    def minimumRemainingProduct(startIndex, remainingExponents):
        product = 1

        for offset, exponent in enumerate(remainingExponents):
            if startIndex + offset >= len(primes):
                return limit + 1

            product *= primes[startIndex + offset] ** exponent

            if product > limit:
                return product

        return product

    @lru_cache(maxsize=None)
    def countPrimeAssignments(exponents, remainingLimit, startIndex):
        if not exponents:
            return 1

        exponent = exponents[0]
        remainingExponents = exponents[1:]

        if not remainingExponents:
            bound = integerRoot(remainingLimit, exponent)
            return max(0, bisect.bisect_right(primes, bound) - startIndex)

        total = 0
        primeIndex = startIndex

        while primeIndex < len(primes):
            prime = primes[primeIndex]
            primePower = prime**exponent

            if primePower > remainingLimit:
                break

            nextLimit = remainingLimit // primePower

            if minimumRemainingProduct(primeIndex + 1, remainingExponents) > nextLimit:
                break

            total += countPrimeAssignments(remainingExponents, nextLimit, primeIndex + 1)
            primeIndex += 1

        return total

    total = 1

    for pattern in patterns:
        antichainLength = maximumAntichainLengthFromExponents(pattern)
        patternCount = 0

        for orderedExponents in set(itertools.permutations(pattern)):
            patternCount += countPrimeAssignments(orderedExponents, limit, 0)

        total += antichainLength * patternCount

    return total


def maximumAntichainSumBrute(limit):
    return sum(maximumAntichainLength(number) for number in range(1, limit + 1))


def runTests():
    assert maximumAntichainLength(1) == 1
    assert maximumAntichainLength(30) == 3
    assert maximumAntichainSum(30) == maximumAntichainSumBrute(30)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumAntichainSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
