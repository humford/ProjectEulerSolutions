import time
from bisect import bisect_right
from functools import lru_cache
from math import isqrt


MAX_DISTANCE = 5 * 10**11
TARGET_CELL_COUNT = 450


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)

    if limit >= 0:
        sieve[0] = 0

    if limit >= 1:
        sieve[1] = 0

    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start::prime] = b"\x00" * (((limit - start) // prime) + 1)

    return sieve


def factor(number):
    factors = {}
    divisor = 2

    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            number //= divisor

        divisor += 1 if divisor == 2 else 2

    if number > 1:
        factors[number] = factors.get(number, 0) + 1

    return factors


def honeycombPointCountSquared(distanceSquared):
    if distanceSquared % 3 != 0:
        return 0

    factors = factor(distanceSquared)
    total = 6

    for prime, exponent in factors.items():
        if prime == 3:
            continue

        if prime % 3 == 1:
            total *= exponent + 1
        elif exponent % 2 == 1:
            return 0

    return total


def exponentPatterns(product):
    patterns = []

    def search(remaining, minimumFactor, current):
        if remaining == 1:
            patterns.append(tuple(factor - 1 for factor in reversed(current)))
            return

        for factor in range(minimumFactor, remaining + 1):
            if remaining % factor == 0:
                search(remaining // factor, factor, current + [factor])

    search(product, 2, [])

    return patterns


def integerRoot(number, exponent):
    root = int(number ** (1 / exponent))

    while (root + 1) ** exponent <= number:
        root += 1

    while root**exponent > number:
        root -= 1

    return root


def twoModThreeSmoothPrefix(limit, primeFlags):
    smooth = bytearray(b"\x01") * (limit + 1)

    if limit >= 0:
        smooth[0] = 0

    if limit >= 3:
        smooth[3::3] = b"\x00" * (((limit - 3) // 3) + 1)

    for prime in range(7, limit + 1):
        if primeFlags[prime] and prime % 3 == 1:
            smooth[prime::prime] = b"\x00" * (((limit - prime) // prime) + 1)

    prefix = [0] * (limit + 1)
    total = 0

    for number in range(1, limit + 1):
        total += smooth[number]
        prefix[number] = total

    return prefix


def honeycombDistanceCount():
    if TARGET_CELL_COUNT % 6 != 0:
        return 0

    representationProduct = TARGET_CELL_COUNT // 6
    patterns = exponentPatterns(representationProduct)
    assert sorted(patterns) == [(4, 4, 2), (14, 4), (24, 2), (74,)]

    normLimit = MAX_DISTANCE * MAX_DISTANCE // 3
    maxOneModThreePrime = isqrt(normLimit // (7**4 * 13**4))
    primeFlags = primeSieve(maxOneModThreePrime)
    oneModThreePrimes = [
        prime
        for prime in range(7, maxOneModThreePrime + 1)
        if primeFlags[prime] and prime % 3 == 1
    ]
    minimumPatternBase = 7**4 * 13**4 * 19**2
    maxSmooth = isqrt(normLimit // minimumPatternBase)
    smoothPrefix = twoModThreeSmoothPrefix(maxSmooth, primeFlags)

    @lru_cache(maxsize=None)
    def freeMultiplierCount(limit):
        total = 0

        while limit:
            total += smoothPrefix[isqrt(limit)]
            limit //= 3

        return total

    total = 0

    for prime1 in oneModThreePrimes:
        primePower = prime1**24

        if primePower * 7**2 > normLimit:
            break

        maxPrime2 = isqrt(normLimit // primePower)

        for prime2 in oneModThreePrimes[:bisect_right(oneModThreePrimes, maxPrime2)]:
            if prime2 != prime1:
                total += freeMultiplierCount(normLimit // (primePower * prime2**2))

    for prime1 in oneModThreePrimes:
        primePower = prime1**14

        if primePower * 7**4 > normLimit:
            break

        maxPrime2 = integerRoot(normLimit // primePower, 4)

        for prime2 in oneModThreePrimes[:bisect_right(oneModThreePrimes, maxPrime2)]:
            if prime2 != prime1:
                total += freeMultiplierCount(normLimit // (primePower * prime2**4))

    for index1, prime1 in enumerate(oneModThreePrimes):
        primePower1 = prime1**4

        if primePower1 * 13**4 * 7**2 > normLimit:
            break

        for prime2 in oneModThreePrimes[index1 + 1 :]:
            base = primePower1 * prime2**4

            if base * 7**2 > normLimit:
                break

            maxPrime3 = isqrt(normLimit // base)

            for prime3 in oneModThreePrimes[
                : bisect_right(oneModThreePrimes, maxPrime3)
            ]:
                if prime3 != prime1 and prime3 != prime2:
                    total += freeMultiplierCount(normLimit // (base * prime3**2))

    return total


def runTests():
    assert honeycombPointCountSquared(3) == 6
    assert honeycombPointCountSquared(21) == 12
    assert honeycombPointCountSquared(111111111**2) == 54
    assert honeycombPointCountSquared(1) == 0


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = honeycombDistanceCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
