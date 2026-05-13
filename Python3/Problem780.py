import time
from math import gcd, isqrt


MOD = 1_000_000_007


def floorSqrt3Mul(n):
    return isqrt(3 * n * n)


def floorDivSqrt3(n, multiplier):
    numerator = n * n
    denominator = 3 * multiplier * multiplier
    result = isqrt(numerator // denominator)

    while denominator * (result + 1) * (result + 1) <= numerator:
        result += 1
    while denominator * result * result > numerator:
        result -= 1
    return result


def divisorSummatory(n):
    total = 0
    first = 1
    while first <= n:
        quotient = n // first
        last = n // quotient
        total += quotient * (last - first + 1)
        first = last + 1
    return total


def sieveMobiusSmallestPrimeFactor(limit):
    smallestPrimeFactor = [0] * (limit + 1)
    mobius = [0] * (limit + 1)
    primes = []
    mobius[1] = 1

    for n in range(2, limit + 1):
        if smallestPrimeFactor[n] == 0:
            smallestPrimeFactor[n] = n
            primes.append(n)
            mobius[n] = -1
        for prime in primes:
            value = n * prime
            if value > limit:
                break
            smallestPrimeFactor[value] = prime
            if n % prime == 0:
                mobius[value] = 0
                break
            mobius[value] = -mobius[n]

    if limit >= 1:
        smallestPrimeFactor[1] = 1
    return smallestPrimeFactor, mobius


def distinctPrimeFactors(n, smallestPrimeFactor):
    factors = []
    while n > 1:
        prime = smallestPrimeFactor[n]
        factors.append(prime)
        while n % prime == 0:
            n //= prime
    return factors


def buildSquarefreeDivisors(limit, smallestPrimeFactor):
    squarefreeDivisors = [None] * (limit + 1)
    squarefreeDivisors[1] = [(1, 1)]

    for n in range(2, limit + 1):
        divisors = [(1, 1)]
        for prime in distinctPrimeFactors(n, smallestPrimeFactor):
            divisors += [(divisor * prime, -sign) for divisor, sign in divisors]
        squarefreeDivisors[n] = divisors

    return squarefreeDivisors


def buildAllDivisors(limit, smallestPrimeFactor):
    allDivisors = [None] * (limit + 1)
    allDivisors[1] = [1]

    for n in range(2, limit + 1):
        reduced = n
        prime = smallestPrimeFactor[reduced]
        exponent = 0
        while reduced % prime == 0:
            reduced //= prime
            exponent += 1

        divisors = []
        power = 1
        for _ in range(exponent + 1):
            for divisor in allDivisors[reduced]:
                divisors.append(divisor * power)
            power *= prime
        allDivisors[n] = divisors

    return allDivisors


def normalizeAlpha(a, b, c):
    if c < 0:
        a, b, c = -a, -b, -c
    divisor = gcd(gcd(abs(a), abs(b)), c)
    if divisor > 1:
        a //= divisor
        b //= divisor
        c //= divisor
    return a, b, c


def floorQuadraticSqrt3(a, b, c):
    if b == 0:
        return a // c

    result = (a + floorSqrt3Mul(b)) // c
    threeBSquared = 3 * b * b

    while True:
        value = (result + 1) * c - a
        if value <= 0 or value * value <= threeBSquared:
            result += 1
        else:
            break

    while True:
        value = result * c - a
        if value <= 0 or value * value <= threeBSquared:
            break
        result -= 1

    return result


def alphaFloor(alpha):
    a, b, c = alpha
    return floorQuadraticSqrt3(a, b, c)


def alphaMulFloor(alpha, n):
    a, b, c = alpha
    return floorQuadraticSqrt3(a * n, b * n, c)


def alphaSubInt(alpha, integer):
    a, b, c = alpha
    return normalizeAlpha(a - integer * c, b, c)


def alphaDivAlphaMinusOne(alpha):
    a, b, c = alpha
    shiftedA = a - c

    numeratorA = a * shiftedA - 3 * b * b
    numeratorB = -b * c
    denominator = shiftedA * shiftedA - 3 * b * b

    if denominator < 0:
        numeratorA, numeratorB, denominator = -numeratorA, -numeratorB, -denominator
    if numeratorB < 0:
        numeratorA, numeratorB = -numeratorA, -numeratorB

    return normalizeAlpha(numeratorA, numeratorB, denominator)


def triangle(n):
    return n * (n + 1) // 2


def beattySum(alpha, n):
    total = 0
    sign = 1

    while n > 0:
        integerPart = alphaFloor(alpha)
        if integerPart > 1:
            total += sign * (integerPart - 1) * triangle(n)
            alpha = alphaSubInt(alpha, integerPart - 1)

        m = alphaMulFloor(alpha, n)
        total += sign * triangle(m)

        n = m - n
        if n <= 0:
            break

        alpha = alphaDivAlphaMinusOne(alpha)
        sign = -sign

    return total


def beattySqrt3(coefficient, n):
    if n <= 0:
        return 0
    return beattySum((0, coefficient, 1), n)


def stripHyperbolaSum(N, V, L, squarefreeDivisors, allDivisors):
    sum1 = 0
    sum2 = 0

    for v in range(1, V + 1):
        maxU = L // v
        for divisor in allDivisors[v]:
            reducedV = v // divisor
            high = maxU // divisor
            if high < reducedV:
                continue

            weight = N // (2 * divisor)
            lowMinusOne = reducedV - 1
            count = 0
            beattyTotal = 0

            for q, mobius in squarefreeDivisors[reducedV]:
                count += mobius * (high // q - lowMinusOne // q)

                highQ = high // q
                lowQ = lowMinusOne // q
                if highQ:
                    beattyTotal += mobius * (
                        beattySqrt3(v * q, highQ) - beattySqrt3(v * q, lowQ)
                    )

            sum1 += weight * count
            sum2 += beattyTotal

    diagonal1 = 0
    diagonal2 = 0
    for v in range(1, V + 1):
        diagonal1 += N // (2 * v)
        diagonal2 += floorSqrt3Mul(v)

    return 2 * sum1 - diagonal1, 2 * sum2 - diagonal2


def countMod3Residue(low, high, residue):
    if high < low:
        return 0
    first = low + (residue - low % 3) % 3
    if first > high:
        return 0
    return (high - first) // 3 + 1


def hexSummatory(limit, squarefreeDivisors, divisorCache):
    if limit <= 0:
        return 0

    def cachedDivisorSummatory(n):
        value = divisorCache.get(n)
        if value is None:
            value = divisorSummatory(n)
            divisorCache[n] = value
        return value

    maxV = isqrt(limit)
    extra = 0

    for v in range(1, maxV + 1):
        discriminant = 4 * limit - 3 * v * v
        if discriminant <= 0:
            break

        maxU = (-v + isqrt(discriminant)) // 2
        u = v + 1
        squarefreeV = squarefreeDivisors[v]
        vMod3 = v % 3

        while u <= maxU:
            norm = u * u + u * v + v * v
            quotient = limit // norm
            if quotient == 0:
                break

            threshold = limit // quotient
            nextDiscriminant = 4 * threshold - 3 * v * v
            highU = (-v + isqrt(nextDiscriminant)) // 2
            highU = min(highU, maxU)

            lowMinusOne = u - 1
            count = 0
            for divisor, mobius in squarefreeV:
                count += mobius * (highU // divisor - lowMinusOne // divisor)

            if vMod3 != 0:
                bad = 0
                for divisor, mobius in squarefreeV:
                    inverse = 1 if divisor % 3 == 1 else 2
                    lowT = (u + divisor - 1) // divisor
                    highT = highU // divisor
                    residue = (vMod3 * inverse) % 3
                    bad += mobius * countMod3Residue(lowT, highT, residue)
                count -= bad

            if count:
                extra += count * cachedDivisorSummatory(quotient)

            u = highU + 1

    return cachedDivisorSummatory(limit) + 2 * extra


def G(N):
    if N <= 0:
        return 0

    halfN = N // 2
    stripLimit = floorDivSqrt3(halfN, 1)
    maxStripV = isqrt(stripLimit)
    hexLimit = N // 4
    maxHexV = isqrt(hexLimit) if hexLimit > 0 else 0

    precomputeLimit = max(maxStripV, maxHexV, 1)
    smallestPrimeFactor, _ = sieveMobiusSmallestPrimeFactor(precomputeLimit)
    squarefreeDivisors = buildSquarefreeDivisors(precomputeLimit, smallestPrimeFactor)
    allDivisors = buildAllDivisors(precomputeLimit, smallestPrimeFactor)

    base = 2 * divisorSummatory(halfN)
    strip1, strip2 = stripHyperbolaSum(N, maxStripV, stripLimit, squarefreeDivisors, allDivisors)
    stripPart = base + 4 * (strip1 - strip2)

    hexPart = hexSummatory(hexLimit, squarefreeDivisors, {})
    return (stripPart - 4 * hexPart) % MOD


def runTests():
    assert floorSqrt3Mul(10) == 17
    assert floorDivSqrt3(100, 1) == 57
    assert divisorSummatory(10) == 27
    assert G(6) == 14
    assert G(100) == 8090
    assert G(100_000) == 645_124_048


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = G(10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
