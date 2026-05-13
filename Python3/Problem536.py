from bisect import bisect_right
from math import gcd, isqrt
import time


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

    smallPrimes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in smallPrimes:
        if n % p == 0:
            return n == p

    d = n - 1
    shifts = 0
    while d % 2 == 0:
        shifts += 1
        d //= 2

    for base in (2, 3, 5, 7, 11, 13):
        if base >= n:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(shifts - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def factorNumber(n, primes):
    factors = []
    remaining = n
    for p in primes:
        if p * p > remaining:
            break
        if remaining % p == 0:
            exponent = 0
            while remaining % p == 0:
                remaining //= p
                exponent += 1
            factors.append((p, exponent))
    if remaining > 1:
        factors.append((remaining, 1))
    return factors


def divisorsFromFactors(factors):
    divisors = [1]
    for p, exponent in factors:
        baseDivisors = list(divisors)
        multiplier = 1
        for _ in range(exponent):
            multiplier *= p
            divisors.extend(d * multiplier for d in baseDivisors)
    return divisors


def solveLinearCongruence(coefficient, residue, modulus):
    if modulus == 1:
        return 0, 1

    common = gcd(coefficient, modulus)
    if residue % common != 0:
        return None

    coefficient //= common
    residue //= common
    modulus //= common
    return (residue * pow(coefficient, -1, modulus)) % modulus, modulus


def combineCongruences(residueA, modulusA, residueB, modulusB):
    if modulusA == 1:
        return residueB % modulusB, modulusB
    if modulusB == 1:
        return residueA % modulusA, modulusA

    common = gcd(modulusA, modulusB)
    difference = residueB - residueA
    if difference % common != 0:
        return None

    reducedModulus = modulusB // common
    scale = (
        (difference // common)
        * pow(modulusA // common, -1, reducedModulus)
    ) % reducedModulus
    combinedModulus = modulusA * reducedModulus
    return (residueA + modulusA * scale) % combinedModulus, combinedModulus


def hasSmallPositiveSolution(residue, modulus, limit):
    if limit < 1:
        return False
    smallest = 1 if modulus == 1 else (residue if residue else modulus)
    return smallest <= limit


def moduloPowerIdentityValues(limit):
    primes = primeSieve(isqrt(limit) + 5)
    values = set()

    def addValue(value):
        if value <= limit:
            values.add(value)

    def addFinalPrimeExtensions(product, startIndex, residue, modulus, remaining, smallLimit):
        lastPrime = primes[startIndex - 1] if startIndex else 1
        for divisor in divisorsFromFactors(factorNumber(product + 3, primes)):
            p = divisor + 1
            if p <= smallLimit or p <= lastPrime or p > remaining:
                continue
            if p % modulus != residue % modulus:
                continue
            if isPrime(p):
                addValue(product * p)

    def search(product, startIndex, residue, modulus):
        remaining = limit // product
        if 1 % modulus == residue % modulus:
            addValue(product)

        smallLimit = min(remaining, isqrt(remaining))
        addFinalPrimeExtensions(product, startIndex, residue, modulus, remaining, smallLimit)

        endIndex = bisect_right(primes, smallLimit)
        for index in range(startIndex, endIndex):
            p = primes[index]

            existingConstraint = solveLinearCongruence(p, residue, modulus)
            if existingConstraint is None:
                continue

            newConstraint = solveLinearCongruence(
                product % (p - 1),
                (-3) % (p - 1),
                p - 1,
            )
            if newConstraint is None:
                continue

            combinedConstraint = combineCongruences(
                existingConstraint[0],
                existingConstraint[1],
                newConstraint[0],
                newConstraint[1],
            )
            if combinedConstraint is None:
                continue

            nextResidue, nextModulus = combinedConstraint
            if hasSmallPositiveSolution(nextResidue, nextModulus, remaining // p):
                search(product * p, index + 1, nextResidue, nextModulus)

    search(1, 0, 0, 1)
    return sorted(values)


def moduloPowerIdentitySum(limit):
    return sum(moduloPowerIdentityValues(limit))


def runTests():
    assert moduloPowerIdentityValues(100) == [1, 2, 3, 5, 21]
    assert moduloPowerIdentitySum(100) == 32
    assert moduloPowerIdentitySum(10 ** 6) == 22_868_117


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = moduloPowerIdentitySum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
