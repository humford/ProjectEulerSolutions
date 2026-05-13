import math
import random
import time


MAX_K = 41


def polynomialDegree(poly):
    return poly.bit_length() - 1


def polynomialMod(poly, modulus):
    modulusDegree = polynomialDegree(modulus)
    while poly and polynomialDegree(poly) >= modulusDegree:
        poly ^= modulus << (polynomialDegree(poly) - modulusDegree)
    return poly


def polynomialMultiply(left, right):
    result = 0
    while right:
        bit = right & -right
        result ^= left << (bit.bit_length() - 1)
        right ^= bit
    return result


def polynomialMultiplyMod(left, right, modulus):
    return polynomialMod(polynomialMultiply(left, right), modulus)


SQUARE_TABLE = [0] * 256
for byte in range(256):
    value = 0
    for bit in range(8):
        if (byte >> bit) & 1:
            value |= 1 << (2 * bit)
    SQUARE_TABLE[byte] = value


def polynomialSquare(poly):
    result = 0
    shift = 0
    while poly:
        result |= SQUARE_TABLE[poly & 0xFF] << (16 * shift)
        poly >>= 8
        shift += 1
    return result


def polynomialSquareMod(poly, modulus):
    return polynomialMod(polynomialSquare(poly), modulus)


def polynomialPowerMod(poly, exponent, modulus):
    result = 1
    base = polynomialMod(poly, modulus)

    while exponent:
        if exponent % 2:
            result = polynomialMultiplyMod(result, base, modulus)
        exponent //= 2
        if exponent:
            base = polynomialSquareMod(base, modulus)

    return result


def polynomialGcd(left, right):
    while right:
        left, right = right, polynomialMod(left, right)
    return left


def polynomialDivideExact(poly, divisor):
    divisorDegree = polynomialDegree(divisor)
    quotient = 0

    while poly and polynomialDegree(poly) >= divisorDegree:
        shift = polynomialDegree(poly) - divisorDegree
        quotient ^= 1 << shift
        poly ^= divisor << shift

    assert poly == 0
    return quotient


def integerLcm(a, b):
    return a // math.gcd(a, b) * b


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if isPrime[p]:
            isPrime[p * p:limit + 1:p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [n for n in range(limit + 1) if isPrime[n]]


SMALL_PRIMES = primeSieve(math.isqrt((1 << MAX_K) - 1) + 1)
MERSENNE_FACTOR_CACHE = {}
POLY_FACTOR_CACHE = {}
FACTOR_CACHE_BY_ODD_PART = {}


def factorSmall(n):
    factors = []
    remaining = n

    for prime in SMALL_PRIMES:
        if prime * prime > remaining:
            break
        while remaining % prime == 0:
            factors.append(prime)
            remaining //= prime

    if remaining > 1:
        factors.append(remaining)
    return factors


def mersenneFactors(k):
    cached = MERSENNE_FACTOR_CACHE.get(k)
    if cached is not None:
        return list(cached)

    factors = sorted(factorSmall((1 << k) - 1))
    MERSENNE_FACTOR_CACHE[k] = factors
    return list(factors)


def berlekampNullspaceBasis(poly):
    degree = polynomialDegree(poly)
    rows = [0] * degree

    for column in range(degree):
        value = polynomialMod(1 << (2 * column), poly)
        row = 0
        while value:
            if value & 1:
                rows[row] |= 1 << column
            value >>= 1
            row += 1

    for i in range(degree):
        rows[i] ^= 1 << i

    pivotColumns = []
    pivotRowForColumn = {}
    rank = 0

    for column in range(degree):
        pivot = None
        for row in range(rank, degree):
            if (rows[row] >> column) & 1:
                pivot = row
                break
        if pivot is None:
            continue

        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivotRow = rows[rank]
        for row in range(degree):
            if row != rank and ((rows[row] >> column) & 1):
                rows[row] ^= pivotRow

        pivotColumns.append(column)
        pivotRowForColumn[column] = rank
        rank += 1

    pivotSet = set(pivotColumns)
    basis = []

    for freeColumn in range(degree):
        if freeColumn in pivotSet:
            continue
        value = 1 << freeColumn
        for pivotColumn in pivotColumns:
            row = rows[pivotRowForColumn[pivotColumn]]
            if (row >> freeColumn) & 1:
                value |= 1 << pivotColumn
        basis.append(value)

    return basis


def factorSquarefree(poly):
    if poly == 1:
        return []
    if polynomialDegree(poly) <= 1:
        return [poly]

    basis = berlekampNullspaceBasis(poly)
    if len(basis) == 1:
        return [poly]

    for _ in range(300):
        combination = 0
        for value in basis[1:]:
            if random.getrandbits(1):
                combination ^= value
        if combination in (0, 1):
            continue

        gcdValue = polynomialGcd(poly, combination)
        if gcdValue not in (1, poly):
            other = polynomialDivideExact(poly, gcdValue)
            return factorSquarefree(gcdValue) + factorSquarefree(other)

        gcdValue = polynomialGcd(poly, combination ^ 1)
        if gcdValue not in (1, poly):
            other = polynomialDivideExact(poly, gcdValue)
            return factorSquarefree(gcdValue) + factorSquarefree(other)

    raise RuntimeError("Berlekamp split failed")


def factorPolynomialCached(poly):
    cached = POLY_FACTOR_CACHE.get(poly)
    if cached is not None:
        return list(cached)

    factors = factorSquarefree(poly)
    POLY_FACTOR_CACHE[poly] = factors
    return list(factors)


def irreducibleFactorsXmPlusOne(oddPart):
    cached = FACTOR_CACHE_BY_ODD_PART.get(oddPart)
    if cached is not None:
        return list(cached)

    poly = (1 << oddPart) | 1
    factors = factorPolynomialCached(poly)
    FACTOR_CACHE_BY_ODD_PART[oddPart] = factors
    return list(factors)


def frobeniusOrbitDegree(element, irreducible):
    value = element
    for degree in range(1, polynomialDegree(irreducible) + 1):
        value = polynomialSquareMod(value, irreducible)
        if value == element:
            return degree
    return polynomialDegree(irreducible)


def multiplicativeOrder(element, irreducible):
    if element == 0:
        return 0

    degree = frobeniusOrbitDegree(element, irreducible)
    order = (1 << degree) - 1

    for prime in sorted(set(mersenneFactors(degree))):
        while order % prime == 0:
            candidate = order // prime
            if polynomialPowerMod(element, candidate, irreducible) == 1:
                order = candidate
            else:
                break

    return order


def maxTwoLiftExponent(basePolynomial, oddOrder, factor, maxExponent):
    if maxExponent <= 1:
        return 0

    order = oddOrder
    modulus = factor

    for _ in range(2, maxExponent + 1):
        modulus = polynomialMultiply(modulus, factor)
        while polynomialPowerMod(basePolynomial, order, modulus) != 1:
            order *= 2

    return (order // oddOrder).bit_length() - 1


def periodsForN(n):
    oddPart = n
    twos = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        twos += 1

    maxExponent = 1 << twos
    updatePolynomial = (1 << 1) | (1 << (n - 1))
    periodsByOddLcm = {1: 0}

    for factor in irreducibleFactorsXmPlusOne(oddPart):
        updateModFactor = polynomialMod(updatePolynomial, factor)
        if polynomialGcd(updateModFactor, factor) != 1:
            continue

        oddOrder = multiplicativeOrder(updateModFactor, factor)
        maxTwos = maxTwoLiftExponent(updatePolynomial, oddOrder, factor, maxExponent)
        updated = dict(periodsByOddLcm)

        for currentOdd, currentTwos in periodsByOddLcm.items():
            nextOdd = integerLcm(currentOdd, oddOrder)
            nextTwos = max(currentTwos, maxTwos)
            if nextOdd not in updated or updated[nextOdd] < nextTwos:
                updated[nextOdd] = nextTwos

        periodsByOddLcm = updated

    periods = set()
    for oddPeriod, maxTwos in periodsByOddLcm.items():
        for exponent in range(maxTwos + 1):
            periods.add(oddPeriod << exponent)

    return periods


def S(limit):
    allPeriods = set()
    totalAt = {}

    for n in range(3, limit + 1):
        allPeriods.update(periodsForN(n))
        totalAt[n] = sum(allPeriods)

    return totalAt[limit]


def runTests():
    allPeriods = set()
    s6 = None
    s30 = None

    for n in range(3, 31):
        allPeriods.update(periodsForN(n))
        if n == 6:
            s6 = sum(allPeriods)
        if n == 30:
            s30 = sum(allPeriods)

    assert s6 == 6
    assert s30 == 20_381


def solve():
    return S(100)


if __name__ == "__main__":
    random.seed(0)
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
