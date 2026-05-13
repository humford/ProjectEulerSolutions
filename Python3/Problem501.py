from functools import lru_cache
import bisect
import math
import time


SIEVE_LIMIT = 10_000_000
PHI_CACHE_ROWS = 100
PHI_CACHE_COLUMNS = 100_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)

    return [number for number in range(limit + 1) if sieve[number]]


PRIMES = primeSieve(SIEVE_LIMIT)
PHI_CACHE = [[0] * (PHI_CACHE_COLUMNS + 1) for _ in range(PHI_CACHE_ROWS + 1)]

for value in range(PHI_CACHE_COLUMNS + 1):
    PHI_CACHE[0][value] = value

for row in range(1, PHI_CACHE_ROWS + 1):
    prime = PRIMES[row - 1]
    previous = PHI_CACHE[row - 1]
    current = PHI_CACHE[row]

    for value in range(PHI_CACHE_COLUMNS + 1):
        current[value] = previous[value] - previous[value // prime]


@lru_cache(maxsize=None)
def phi(value, primeCount):
    if primeCount == 0:
        return value

    if primeCount <= PHI_CACHE_ROWS and value <= PHI_CACHE_COLUMNS:
        return PHI_CACHE[primeCount][value]

    return phi(value, primeCount - 1) - phi(value // PRIMES[primeCount - 1], primeCount - 1)


def integerRoot(value, power):
    root = int(value ** (1.0 / power))

    while (root + 1) ** power <= value:
        root += 1

    while root**power > value:
        root -= 1

    return root


@lru_cache(maxsize=None)
def primeCount(limit):
    if limit <= SIEVE_LIMIT:
        return bisect.bisect_right(PRIMES, limit)

    fourthRootCount = primeCount(integerRoot(limit, 4))
    squareRootCount = primeCount(math.isqrt(limit))
    cubeRootCount = primeCount(integerRoot(limit, 3))

    total = phi(limit, fourthRootCount)
    total += ((squareRootCount + fourthRootCount - 2) * (squareRootCount - fourthRootCount + 1)) // 2

    for index in range(fourthRootCount, squareRootCount):
        quotient = limit // PRIMES[index]
        total -= primeCount(quotient)

        if index < cubeRootCount:
            nestedLimit = primeCount(math.isqrt(quotient))
            for nestedIndex in range(index, nestedLimit):
                total -= primeCount(quotient // PRIMES[nestedIndex]) - nestedIndex

    return total


def pToSeventhCount(limit):
    count = 0

    for prime in PRIMES:
        if prime**7 > limit:
            break

        count += 1

    return count


def pCubedTimesQCount(limit):
    count = 0

    for prime in PRIMES:
        primeCubed = prime**3
        if primeCubed > limit:
            break

        maxQ = limit // primeCubed
        count += primeCount(maxQ)
        if prime <= maxQ:
            count -= 1

    return count


def threePrimeProductCount(limit):
    count = 0

    for firstIndex, firstPrime in enumerate(PRIMES):
        if firstPrime**3 > limit:
            break

        maxSecondPrime = math.isqrt(limit // firstPrime)
        secondEnd = bisect.bisect_right(PRIMES, maxSecondPrime)

        for secondIndex in range(firstIndex + 1, secondEnd):
            maxThirdPrime = limit // (firstPrime * PRIMES[secondIndex])
            count += primeCount(maxThirdPrime) - secondIndex - 1

    return count


def eightDivisorCount(limit):
    return pToSeventhCount(limit) + pCubedTimesQCount(limit) + threePrimeProductCount(limit)


def runTests():
    assert eightDivisorCount(100) == 10
    assert eightDivisorCount(1_000) == 180
    assert eightDivisorCount(10**6) == 224_427


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = eightDivisorCount(10**12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
