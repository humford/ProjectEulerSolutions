from math import isqrt
import time


TARGET_POWER = 16
TARGET_LIMIT = 10**TARGET_POWER
SIEVE_LIMIT = 100_000


def primeSieve(limit):
    isPrime = [True] * (limit + 1)
    isPrime[0] = False
    isPrime[1] = False

    for n in range(2, isqrt(limit) + 1):
        if isPrime[n]:
            for multiple in range(n * n, limit + 1, n):
                isPrime[multiple] = False

    return [n for n in range(2, limit + 1) if isPrime[n]]


def smallestPrimeFactors(limit, primes):
    spf = list(range(limit + 1))

    for prime in primes:
        if prime * prime > limit:
            break
        for multiple in range(prime * prime, limit + 1, prime):
            if spf[multiple] == multiple:
                spf[multiple] = prime

    return spf


def factorization(n, spf):
    factors = {}

    while n > 1:
        prime = spf[n]
        exponent = 0
        while n % prime == 0:
            n //= prime
            exponent += 1
        factors[prime] = exponent

    return factors


def generateExponentVectors(limit, primes):
    vectors = []

    def search(primeIndex, maxExponent, current, exponents):
        if exponents:
            vectors.append(tuple(exponents))

        if primeIndex == len(primes):
            return

        prime = primes[primeIndex]
        value = current * prime
        exponent = 1

        while exponent <= maxExponent and value <= limit:
            exponents.append(exponent)
            search(primeIndex + 1, exponent, value, exponents)
            exponents.pop()
            exponent += 1
            value *= prime

    search(0, limit.bit_length(), 1, [])
    return vectors


def divisorCountFromExponents(exponents):
    count = 1
    for exponent in exponents:
        count *= exponent + 1
    return count


def remainingGreedyProduct(exponents, optionalBases, usedMask, limit):
    value = 1
    baseIndex = 0

    for index, exponent in enumerate(exponents):
        if usedMask & (1 << index):
            continue

        value *= optionalBases[baseIndex] ** exponent
        if value > limit:
            return limit + 1
        baseIndex += 1

    return value


def minimalNumberForExponents(exponents, limit, primes, spf):
    divisorCount = divisorCountFromExponents(exponents)
    required = factorization(divisorCount, spf)

    if len(required) > len(exponents):
        return divisorCount, None

    requiredPrimes = set(required)
    optionalBases = []
    for prime in primes:
        if prime not in requiredPrimes:
            optionalBases.append(prime)
            if len(optionalBases) == len(exponents) - len(required):
                break

    # The exponents determine tau(n).  Divisibility by tau(n) only adds lower
    # bounds to the exponents assigned to the prime factors of tau(n).  Once
    # those required primes are placed, the remaining exponents go greedily on
    # the smallest unused optional primes by the rearrangement inequality.
    assignments = {0: 1}
    for requiredPrime in sorted(required, reverse=True):
        minimumExponent = required[requiredPrime]
        powers = [
            requiredPrime ** exponent if exponent >= minimumExponent else None
            for exponent in exponents
        ]
        nextAssignments = {}

        for usedMask, partial in assignments.items():
            for index, primePower in enumerate(powers):
                if primePower is None or usedMask & (1 << index):
                    continue

                candidate = partial * primePower
                if candidate > limit:
                    continue

                nextMask = usedMask | (1 << index)
                if candidate < nextAssignments.get(nextMask, limit + 1):
                    nextAssignments[nextMask] = candidate

        assignments = nextAssignments
        if not assignments:
            return divisorCount, None

    best = None
    for usedMask, partial in assignments.items():
        candidate = partial * remainingGreedyProduct(
            exponents,
            optionalBases,
            usedMask,
            limit,
        )

        if candidate <= limit and (best is None or candidate < best):
            best = candidate

    return divisorCount, best


def minimalTauNumbers(limit):
    primes = primeSieve(SIEVE_LIMIT)
    spf = smallestPrimeFactors(SIEVE_LIMIT, primes)
    best = {1: 1}

    for exponents in generateExponentVectors(limit, primes):
        divisorCount, candidate = minimalNumberForExponents(
            exponents,
            limit,
            primes,
            spf,
        )
        if candidate is not None and candidate < best.get(divisorCount, limit + 1):
            best[divisorCount] = candidate

    return best


def M(power):
    return sum(minimalTauNumbers(10**power).values())


def divisorCount(n):
    total = 1
    remaining = n
    factor = 2

    while factor * factor <= remaining:
        if remaining % factor == 0:
            exponent = 0
            while remaining % factor == 0:
                remaining //= factor
                exponent += 1
            total *= exponent + 1
        factor += 1 if factor == 2 else 2

    if remaining > 1:
        total *= 2

    return total


def bruteM(power):
    limit = 10**power
    best = {1: 1}

    for n in range(2, limit + 1):
        tau = divisorCount(n)
        if n % tau == 0 and n < best.get(tau, limit + 1):
            best[tau] = n

    return sum(best.values())


def solve():
    return M(TARGET_POWER)


def runTests():
    values = minimalTauNumbers(1_000)
    assert divisorCount(12) == 6
    assert values[8] == 24
    assert values[12] == 60
    assert values[16] == 384
    assert bruteM(3) == 3189
    assert M(3) == 3189
    assert solve() == 1_154_027_691_000_533_893


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
