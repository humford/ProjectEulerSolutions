from math import isqrt
import time


TARGET_LIMIT = 100
PRIME_LIMIT = 10_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    primes = []

    for value in range(2, limit + 1):
        if sieve[value]:
            primes.append(value)
            start = value * value
            if start <= limit:
                sieve[start::value] = b"\x00" * (((limit - start) // value) + 1)

    return primes


PRIMES = primeSieve(PRIME_LIMIT)
FACTOR_CACHE = {}


def mergeFactors(left, right):
    result = left.copy()
    for prime, exponent in right.items():
        result[prime] = result.get(prime, 0) + exponent
    return result


def factor(value):
    cached = FACTOR_CACHE.get(value)
    if cached is not None:
        return cached

    remaining = value
    factors = {}

    for prime in PRIMES:
        if prime * prime > remaining:
            break
        while remaining % prime == 0:
            factors[prime] = factors.get(prime, 0) + 1
            remaining //= prime

    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1

    FACTOR_CACHE[value] = factors
    return factors


def factorFourthProductMinusOne(n, m):
    product = n * m
    factors = {}

    for part in (product - 1, product + 1, product * product + 1):
        factors = mergeFactors(factors, factor(part))

    return factors


def divisorsWithFactors(factors):
    items = list(factors.items())
    divisors = []

    def search(index, divisor, divisorFactors):
        if index == len(items):
            divisors.append((divisor, divisorFactors.copy()))
            return

        prime, exponent = items[index]
        value = 1
        for currentExponent in range(exponent + 1):
            if currentExponent:
                divisorFactors[prime] = currentExponent
            else:
                divisorFactors.pop(prime, None)

            search(index + 1, divisor * value, divisorFactors)
            value *= prime

        divisorFactors.pop(prime, None)

    search(0, 1, {})
    return divisors


def phiAndFactorization(factors):
    phi = 1
    phiFactors = {}

    for prime, exponent in factors.items():
        phi *= (prime - 1) * prime ** (exponent - 1)

        if exponent > 1:
            phiFactors[prime] = phiFactors.get(prime, 0) + exponent - 1

        for factorPrime, factorExponent in factor(prime - 1).items():
            phiFactors[factorPrime] = (
                phiFactors.get(factorPrime, 0) + factorExponent
            )

    return phi, phiFactors


def multiplicativeOrder(base, modulus, phi, phiFactors):
    if modulus == 1:
        return 1

    order = phi
    base %= modulus

    for prime in phiFactors:
        while order % prime == 0 and pow(base, order // prime, modulus) == 1:
            order //= prime

    return order


def cycleCountWithoutFinalFixedPoint(columns, modulusFactors):
    total = 0

    for divisor, divisorFactors in divisorsWithFactors(modulusFactors):
        phi, phiFactors = phiAndFactorization(divisorFactors)
        order = multiplicativeOrder(columns, divisor, phi, phiFactors)
        total += phi // order

    return total


def minimalSwaps(rows, columns):
    modulus = rows * columns - 1
    cycles = cycleCountWithoutFinalFixedPoint(columns, factor(modulus))
    return rows * columns - 1 - cycles


def minimalSwapsFourthPowers(n, m):
    rows = n**4
    columns = m**4
    modulusFactors = factorFourthProductMinusOne(n, m)
    cycles = cycleCountWithoutFinalFixedPoint(columns, modulusFactors)
    return rows * columns - 1 - cycles


def sampleSum(limit):
    return sum(
        minimalSwaps(n, m)
        for n in range(2, limit + 1)
        for m in range(n, limit + 1)
    )


def solve():
    return sum(
        minimalSwapsFourthPowers(n, m)
        for n in range(2, TARGET_LIMIT + 1)
        for m in range(n, TARGET_LIMIT + 1)
    )


def runTests():
    assert minimalSwaps(3, 4) == 8
    assert sampleSum(100) == 12_578_833
    assert solve() == 2_101_925_115_560_555_020


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
