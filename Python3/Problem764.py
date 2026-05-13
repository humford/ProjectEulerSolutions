import time
from math import gcd, isqrt


MOD = 1_000_000_000


def fourthRootFloor(n):
    if n <= 0:
        return 0
    return isqrt(isqrt(n))


def fourthRootCeiling(n):
    root = fourthRootFloor(n)
    return root + (root ** 4 < n)


def oddCount(limit):
    if limit <= 0:
        return 0
    return (limit + 1) // 2


def oddSum(limit):
    if limit <= 0:
        return 0
    count = (limit + 1) // 2
    return count * count


def oddFourthPowerSum(limit):
    if limit <= 0:
        return 0
    count = (limit + 1) // 2
    s1 = count * (count + 1) // 2
    s2 = count * (count + 1) * (2 * count + 1) // 6
    s3 = s1 * s1
    s4 = count * (count + 1) * (2 * count + 1) * (3 * count * count + 3 * count - 1) // 30
    return 16 * s4 - 32 * s3 + 24 * s2 - 8 * s1 + count


def smallestPrimeFactorSieve(limit):
    spf = list(range(limit + 1))
    for n in range(2, isqrt(limit) + 1):
        if spf[n] == n:
            for multiple in range(n * n, limit + 1, n):
                if spf[multiple] == multiple:
                    spf[multiple] = n
    return spf


def uniquePrimeFactors(n, spf):
    factors = []
    while n > 1:
        prime = spf[n]
        factors.append(prime)
        while n % prime == 0:
            n //= prime
    return factors


def squarefreeDivisorsWithMu(n, spf, cache):
    if n in cache:
        return cache[n]

    divisors = [(1, 1)]
    for prime in uniquePrimeFactors(n, spf):
        divisors += [(divisor * prime, -mu) for divisor, mu in divisors]

    result = [(divisor, mu, divisor ** 4) for divisor, mu in divisors]
    cache[n] = result
    return result


def coprimeOddPrefix(limit, divisors, modSum, modFourth):
    count = 0
    sumT = 0
    sumT4 = 0
    for divisor, mu, divisor4 in divisors:
        reducedLimit = limit // divisor
        if reducedLimit <= 0:
            continue

        count += mu * oddCount(reducedLimit)
        sumT = (sumT + mu * (divisor % modSum) * (oddSum(reducedLimit) % modSum)) % modSum
        sumT4 = (
            sumT4
            + mu * (divisor4 % modFourth) * (oddFourthPowerSum(reducedLimit) % modFourth)
        ) % modFourth

    return count, sumT % modSum, sumT4 % modFourth


def coprimeOddRange(low, high, divisors, modSum, modFourth):
    if high < low or high <= 0:
        return 0, 0, 0
    upper = coprimeOddPrefix(high, divisors, modSum, modFourth)
    if low <= 1:
        return upper

    lower = coprimeOddPrefix(low - 1, divisors, modSum, modFourth)
    return (
        upper[0] - lower[0],
        (upper[1] - lower[1]) % modSum,
        (upper[2] - lower[2]) % modFourth,
    )


def solutionSum(limit, modulus=MOD, includeCount=False):
    modulus2 = 2 * modulus
    modulus8 = 8 * modulus

    maxParameter = fourthRootFloor(2 * limit) + 2
    spf = smallestPrimeFactorSieve(maxParameter)
    divisorCache = {}
    fourthPowers = [n ** 4 for n in range(maxParameter + 1)]

    total = 0
    totalCount = 0

    # Family A:
    # z - 4x = p^4, z + 4x = q^4, with odd coprime p < q.
    qMax = fourthRootFloor(2 * limit - 1)
    for q in range(1, qMax + 1, 2):
        q4 = fourthPowers[q]
        remainder = 2 * limit - q4
        if remainder <= 0:
            break

        pMax = min(fourthRootFloor(remainder), q - 1, limit // q)
        if q4 <= 8:
            continue
        pMax = min(pMax, fourthRootFloor(q4 - 8))

        low = q4 - 8 * limit
        pMin = fourthRootCeiling(low) if low > 1 else 1
        if pMin % 2 == 0:
            pMin += 1
        if pMin > pMax:
            continue

        divisors = squarefreeDivisorsWithMu(q, spf, divisorCache)
        count, sumP, sumP4Mod8 = coprimeOddRange(pMin, pMax, divisors, modulus, modulus8)
        if count <= 0:
            continue

        totalCount += count
        sumX = (((count % modulus8) * (q4 % modulus8) - sumP4Mod8) % modulus8) // 8
        sumZ = (((sumP4Mod8 % modulus2) + (count % modulus2) * (q4 % modulus2)) % modulus2) // 2
        sumY = (q % modulus) * sumP % modulus
        total = (total + sumX + sumY + sumZ) % modulus

    # Family B: one factor has 2-adic exponent 3 and the other has 4k+1.
    k = 1
    while (1 << (4 * k)) <= limit:
        scale4k = 1 << (4 * k)
        scale4kMinus2 = 1 << (4 * k - 2)
        yScale = 1 << (k + 1)

        qMax = fourthRootFloor((limit - 4) // scale4k) if limit > 4 else 0
        for q in range(1, qMax + 1, 2):
            q4 = fourthPowers[q]
            remaining = limit - scale4k * q4
            if remaining < 4:
                continue

            pMax = min(
                fourthRootFloor(remaining // 4),
                fourthRootFloor(scale4kMinus2 * q4 - 1),
                limit // (yScale * q),
            )
            if pMax <= 0:
                continue

            low = scale4kMinus2 * q4 - limit
            pMin = fourthRootCeiling(low) if low > 1 else 1
            if pMin % 2 == 0:
                pMin += 1
            if pMin > pMax:
                continue

            divisors = squarefreeDivisorsWithMu(q, spf, divisorCache)
            count, sumP, sumP4 = coprimeOddRange(pMin, pMax, divisors, modulus, modulus)
            if count <= 0:
                continue

            totalCount += count
            termP4 = 3 * sumP4 % modulus
            termQ4 = 5 * (scale4kMinus2 % modulus) * (q4 % modulus) * (count % modulus) % modulus
            termPQ = (yScale % modulus) * (q % modulus) * sumP % modulus
            total = (total + termP4 + termQ4 + termPQ) % modulus

        pMaxAll = fourthRootFloor(limit // scale4k)
        for p in range(1, pMaxAll + 1, 2):
            p4 = fourthPowers[p]
            remaining = limit - scale4k * p4
            if remaining < 4:
                continue

            qMax = min(
                fourthRootFloor(remaining // 4),
                limit // (yScale * p),
                fourthRootFloor(limit + scale4kMinus2 * p4),
            )
            qMin = fourthRootCeiling(scale4kMinus2 * p4 + 1)
            if qMin % 2 == 0:
                qMin += 1
            if qMin > qMax:
                continue

            divisors = squarefreeDivisorsWithMu(p, spf, divisorCache)
            count, sumQ, sumQ4 = coprimeOddRange(qMin, qMax, divisors, modulus, modulus)
            if count <= 0:
                continue

            totalCount += count
            termQ4 = 5 * sumQ4 % modulus
            termP4 = 3 * (scale4kMinus2 % modulus) * (p4 % modulus) * (count % modulus) % modulus
            termPQ = (yScale % modulus) * (p % modulus) * sumQ % modulus
            total = (total + termQ4 + termP4 + termPQ) % modulus

        k += 1

    return (total, totalCount) if includeCount else total


def bruteSolutions(limit):
    solutions = []
    for y in range(1, limit + 1):
        y4 = y ** 4
        for x in range(1, limit + 1):
            z2 = 16 * x * x + y4
            z = isqrt(z2)
            if z > limit:
                break
            if z * z == z2 and gcd(gcd(x, y), z) == 1:
                solutions.append((x, y, z))
    return solutions


def runTests():
    solutions100 = bruteSolutions(100)
    assert sorted(solutions100) == [(3, 4, 20), (10, 3, 41)]
    assert sum(x + y + z for x, y, z in solutions100) == 81

    s100, count100 = solutionSum(10 ** 2, includeCount=True)
    assert (s100, count100) == (81, 2)

    s10k, count10k = solutionSum(10 ** 4, includeCount=True)
    assert (s10k, count10k) == (112_851, 26)

    assert solutionSum(10 ** 7) == 248_876_211


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solutionSum(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
