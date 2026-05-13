from functools import lru_cache
from itertools import product
from math import gcd
import time


LIMIT = 10 ** 16
MILLER_RABIN_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def firstPrimesForLimit(limit):
    primes = []
    candidate = 2
    productSoFar = 1

    while productSoFar * candidate <= limit:
        isPrimeCandidate = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                isPrimeCandidate = False
                break

        if isPrimeCandidate:
            primes.append(candidate)
            productSoFar *= candidate

        candidate += 1

    return primes


MINIMAL_PRIMES = firstPrimesForLimit(LIMIT)


def isPrime(n):
    if n < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    shifts = 0
    while d % 2 == 0:
        d //= 2
        shifts += 1

    for base in MILLER_RABIN_BASES:
        if base >= n:
            continue
        value = pow(base, d, n)
        if value == 1 or value == n - 1:
            continue
        for _ in range(shifts - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False

    return True


def pollardRho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    constant = 1
    while True:
        x = 2
        y = 2
        divisor = 1

        while divisor == 1:
            x = (x * x + constant) % n
            y = (y * y + constant) % n
            y = (y * y + constant) % n
            divisor = gcd(abs(x - y), n)

        if divisor != n:
            return divisor

        constant += 1


def factor(n, factors):
    if n == 1:
        return
    if isPrime(n):
        factors.append(n)
        return

    divisor = pollardRho(n)
    factor(divisor, factors)
    factor(n // divisor, factors)


def exponentPattern(n):
    if n == 1:
        return ()

    factors = []
    factor(n, factors)
    counts = {}
    for prime in factors:
        counts[prime] = counts.get(prime, 0) + 1

    return tuple(sorted(counts.values(), reverse=True))


@lru_cache(None)
def gozintaChainsFromExponents(exponents):
    if not exponents:
        return 1

    total = 0
    for divisorExponents in product(*(range(exponent + 1) for exponent in exponents)):
        if divisorExponents == exponents:
            continue
        divisorPattern = tuple(
            sorted((exponent for exponent in divisorExponents if exponent), reverse=True)
        )
        total += gozintaChainsFromExponents(divisorPattern)

    return total


def gozintaChains(n):
    return gozintaChainsFromExponents(exponentPattern(n))


def exponentPatterns(limit):
    patterns = [()]

    def extend(maxExponent, primeIndex, value, current):
        if primeIndex >= len(MINIMAL_PRIMES):
            return

        prime = MINIMAL_PRIMES[primeIndex]
        nextValue = value * prime
        exponent = 1

        while exponent <= maxExponent and nextValue <= limit:
            current.append(exponent)
            patterns.append(tuple(current))
            extend(exponent, primeIndex + 1, nextValue, current)
            current.pop()

            exponent += 1
            nextValue *= prime

    extend(64, 0, 1, [])
    return patterns


def gozintaFixedPointSum(limit):
    total = 0

    for pattern in exponentPatterns(limit):
        chainCount = gozintaChainsFromExponents(pattern)
        if chainCount <= limit and exponentPattern(chainCount) == pattern:
            total += chainCount

    return total


def runTests():
    assert gozintaChains(12) == 8
    assert gozintaChains(48) == 48
    assert gozintaChains(120) == 132
    assert gozintaFixedPointSum(10 ** 6) == 516_961


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gozintaFixedPointSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
