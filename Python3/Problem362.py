import itertools
import math
import time
from bisect import bisect_right
from functools import cache, lru_cache


TARGET = 10_000_000_000
SIEVE_LIMIT = 5_000_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(limit + 1) if sieve[number]]


PRIMES = primeSieve(SIEVE_LIMIT)
SMALL_PRIMES = [prime for prime in PRIMES if prime <= math.isqrt(TARGET)]


def integerRoot(number, degree):
    root = int(number ** (1.0 / degree))
    while (root + 1) ** degree <= number:
        root += 1
    while root ** degree > number:
        root -= 1
    return root


@cache
def phi(number, primeCount):
    if primeCount == 0:
        return number

    return phi(number, primeCount - 1) - phi(
        number // PRIMES[primeCount - 1], primeCount - 1
    )


@cache
def primeCount(limit):
    if limit < 2:
        return 0
    if limit <= SIEVE_LIMIT:
        return bisect_right(PRIMES, limit)

    fourthRootCount = primeCount(integerRoot(limit, 4))
    squareRootCount = primeCount(math.isqrt(limit))
    cubeRootCount = primeCount(integerRoot(limit, 3))
    total = phi(limit, fourthRootCount)
    total += (
        (squareRootCount + fourthRootCount - 2)
        * (squareRootCount - fourthRootCount + 1)
        // 2
    )

    for primeIndex in range(fourthRootCount, squareRootCount):
        quotient = limit // PRIMES[primeIndex]
        total -= primeCount(quotient)

        if primeIndex < cubeRootCount:
            quotientRootCount = primeCount(math.isqrt(quotient))
            for secondIndex in range(primeIndex, quotientRootCount):
                total -= primeCount(quotient // PRIMES[secondIndex]) - secondIndex

    return total


def squarefree(number):
    divisor = 2

    while divisor * divisor <= number:
        square = divisor * divisor

        if number % square == 0:
            return False

        divisor += 1

    return number > 1


@lru_cache(None)
def bruteSquarefreeFactorCount(number, minimumFactor=2):
    total = 0

    for factor in range(minimumFactor, number + 1):
        if number % factor == 0 and squarefree(factor):
            quotient = number // factor

            if quotient == 1:
                total += 1
            else:
                total += bruteSquarefreeFactorCount(quotient, factor)

    return total


def bruteSquarefreeFactorSum(limit):
    return sum(bruteSquarefreeFactorCount(number, 2) for number in range(2, limit + 1))


def exponentPatterns(limit):
    patterns = []

    def search(maxExponent, primeIndex, minimumProduct, pattern):
        if primeIndex >= len(SMALL_PRIMES):
            return

        prime = SMALL_PRIMES[primeIndex]
        for exponent in range(maxExponent, 0, -1):
            nextProduct = minimumProduct * prime ** exponent
            if nextProduct <= limit:
                nextPattern = pattern + (exponent,)
                patterns.append(nextPattern)
                search(exponent, primeIndex + 1, nextProduct, nextPattern)

    search(limit.bit_length() - 1, 0, 1, tuple())
    return patterns


@cache
def squarefreeFactorizationsForExponents(exponents):
    rank = len(exponents)

    @cache
    def countFrom(minimumMask, remaining):
        if not any(remaining):
            return 1

        total = 0
        for mask in range(minimumMask, 1 << rank):
            nextRemaining = list(remaining)
            isUsable = True

            for index in range(rank):
                if mask & (1 << index):
                    if nextRemaining[index] == 0:
                        isUsable = False
                        break
                    nextRemaining[index] -= 1

            if isUsable:
                total += countFrom(mask, tuple(nextRemaining))

        return total

    return countFrom(1, tuple(exponents))


@cache
def squarefreeProductCountFrom(limit, factorCount, startPrimeIndex):
    if factorCount == 0:
        return 1
    if factorCount == 1:
        return max(0, primeCount(limit) - startPrimeIndex)

    total = 0
    for primeIndex in range(startPrimeIndex, len(SMALL_PRIMES)):
        prime = SMALL_PRIMES[primeIndex]
        if prime ** factorCount > limit:
            break

        total += squarefreeProductCountFrom(
            limit // prime, factorCount - 1, primeIndex + 1
        )

    return total


@cache
def squarefreeProductCountAvoiding(limit, factorCount, forbiddenPrimeIndices):
    forbiddenPrimeIndices = tuple(
        primeIndex
        for primeIndex in forbiddenPrimeIndices
        if SMALL_PRIMES[primeIndex] <= limit
    )

    if factorCount == 0:
        return 1
    if not forbiddenPrimeIndices:
        return squarefreeProductCountFrom(limit, factorCount, 0)

    primeIndex = forbiddenPrimeIndices[-1]
    smallerForbiddenSet = forbiddenPrimeIndices[:-1]
    withoutPrime = squarefreeProductCountAvoiding(
        limit, factorCount, smallerForbiddenSet
    )
    withPrime = squarefreeProductCountAvoiding(
        limit // SMALL_PRIMES[primeIndex], factorCount - 1, forbiddenPrimeIndices
    )
    return withoutPrime - withPrime


def patternNumberCount(exponents, limit):
    exponents = tuple(exponents)

    @lru_cache(None)
    def search(position, remainingLimit, usedPrimeIndices, previousPrimeIndex):
        if position == len(exponents):
            return 1

        exponent = exponents[position]
        if exponent == 1:
            return squarefreeProductCountAvoiding(
                remainingLimit, len(exponents) - position, usedPrimeIndices
            )

        usedPrimeSet = set(usedPrimeIndices)
        if position > 0 and exponents[position - 1] == exponent:
            startPrimeIndex = previousPrimeIndex + 1
        else:
            startPrimeIndex = 0

        total = 0
        for primeIndex in range(startPrimeIndex, len(SMALL_PRIMES)):
            primePower = SMALL_PRIMES[primeIndex] ** exponent
            if primePower > remainingLimit:
                break
            if primeIndex in usedPrimeSet:
                continue

            nextUsedPrimeIndices = tuple(sorted(usedPrimeSet | {primeIndex}))
            total += search(
                position + 1,
                remainingLimit // primePower,
                nextUsedPrimeIndices,
                primeIndex,
            )

        return total

    return search(0, limit, tuple(), -1)


def squarefreeFactorSum(limit):
    total = 0

    for exponents in exponentPatterns(limit):
        total += squarefreeFactorizationsForExponents(exponents) * patternNumberCount(
            exponents, limit
        )

    return total


def bruteSquarefreeProductCount(limit, factorCount, forbiddenPrimeIndices=()):
    forbiddenPrimeSet = {SMALL_PRIMES[index] for index in forbiddenPrimeIndices}
    usablePrimes = [
        prime
        for prime in SMALL_PRIMES
        if prime <= limit and prime not in forbiddenPrimeSet
    ]
    total = 0

    for combination in itertools.combinations(usablePrimes, factorCount):
        product = 1
        for prime in combination:
            product *= prime
        if product <= limit:
            total += 1

    return total


def runTests():
    assert bruteSquarefreeFactorCount(54, 2) == 2
    assert bruteSquarefreeFactorSum(100) == 193
    assert squarefreeFactorSum(100) == 193
    assert squarefreeProductCountAvoiding(100, 1, tuple()) == bruteSquarefreeProductCount(
        100, 1
    )
    assert squarefreeProductCountAvoiding(100, 2, tuple()) == bruteSquarefreeProductCount(
        100, 2
    )
    assert squarefreeProductCountAvoiding(
        100, 2, (0, 1)
    ) == bruteSquarefreeProductCount(100, 2, (0, 1))


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = squarefreeFactorSum(TARGET)
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
