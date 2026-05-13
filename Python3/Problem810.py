import math
import time


def xorProduct(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def mobius(n):
    remaining = n
    result = 1
    prime = 2

    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            result = -result
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1

    if remaining > 1:
        result = -result

    return result


def divisors(n):
    result = []
    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            result.append(d)
            if d * d != n:
                result.append(n // d)
    return result


def irreduciblePolynomialCount(degree):
    total = 0
    for d in divisors(degree):
        total += mobius(d) * (1 << (degree // d))
    return total // degree


def degreeForRank(rank):
    total = 0
    degree = 1

    while True:
        total += irreduciblePolynomialCount(degree)
        if total >= rank:
            return degree
        degree += 1


def lowbitShiftTable(maxVariableBits):
    table = bytearray(1 << maxVariableBits)
    for n in range(1, len(table)):
        table[n] = (n & -n).bit_length()
    return table


def markMultiples(poly, maxDegree, composite, lowbitShifts):
    degree = poly.bit_length() - 1
    maxCofactorDegree = maxDegree - degree
    if maxCofactorDegree < degree:
        return

    shifted = [poly << shift for shift in range(maxCofactorDegree + 1)]

    for cofactorDegree in range(degree, maxCofactorDegree + 1):
        product = (poly << cofactorDegree) ^ poly
        composite[product >> 1] = 1

        for step in range(1, 1 << (cofactorDegree - 1)):
            product ^= shifted[lowbitShifts[step]]
            composite[product >> 1] = 1


def nthXorPrime(rank):
    if rank == 1:
        return 2

    maxDegree = degreeForRank(rank)
    limit = 1 << (maxDegree + 1)
    composite = bytearray(1 << maxDegree)
    composite[0] = 1

    maxVariableBits = max(0, maxDegree - 2)
    lowbitShifts = lowbitShiftTable(maxVariableBits)

    count = 1
    for candidate in range(3, limit, 2):
        if composite[candidate >> 1]:
            continue

        count += 1
        if count == rank:
            return candidate

        markMultiples(candidate, maxDegree, composite, lowbitShifts)

    raise RuntimeError("Search bound was too small")


def isXorPrimeBruteforce(n):
    if n <= 1:
        return False

    for a in range(2, n):
        for b in range(2, n):
            if xorProduct(a, b) == n:
                return False

    return True


def runTests():
    assert xorProduct(7, 3) == 9
    assert xorProduct(3, 3) == 5

    primes = []
    candidate = 2
    while len(primes) < 10:
        if isXorPrimeBruteforce(candidate):
            primes.append(candidate)
        candidate += 1

    assert primes[:5] == [2, 3, 7, 11, 13]
    assert nthXorPrime(10) == 41


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nthXorPrime(5_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
