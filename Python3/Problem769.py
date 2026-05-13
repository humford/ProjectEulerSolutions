import math
import time
from array import array


SQRT3 = math.sqrt(3.0)
INVERSE_MOD_13 = [0] * 13
for residue in range(1, 13):
    INVERSE_MOD_13[residue] = pow(residue, -1, 13)


def smallestPrimeFactorSieve(limit):
    spf = array("I", [0]) * (limit + 1)
    primes = []
    for n in range(2, limit + 1):
        if spf[n] == 0:
            spf[n] = n
            primes.append(n)
        smallest = spf[n]
        for prime in primes:
            value = n * prime
            if value > limit:
                break
            spf[value] = prime
            if prime == smallest:
                break
    return spf


def distinctPrimeFactors(n, spf):
    factors = []
    while n > 1:
        prime = spf[n]
        factors.append(prime)
        while n % prime == 0:
            n //= prime
    return factors


def squarefreeDivisorsAndMu(n, spf):
    divisors = [1]
    mobius = [1]
    for prime in distinctPrimeFactors(n, spf):
        length = len(divisors)
        for i in range(length):
            divisors.append(divisors[i] * prime)
            mobius.append(-mobius[i])
    return divisors, mobius


def countCoprimeInterval(n, low, high, spf):
    divisors, mobius = squarefreeDivisorsAndMu(n, spf)
    belowLow = low - 1
    total = 0
    for divisor, mu in zip(divisors, mobius):
        total += mu * (high // divisor - belowLow // divisor)
    return total, divisors, mobius


def countResidueInInterval(low, high, modulus, residue):
    if residue < low:
        residue += ((low - residue + modulus - 1) // modulus) * modulus
    if residue > high:
        return 0
    return 1 + (high - residue) // modulus


def countCoprimeWithMod13(divisors, mobius, low, high, residue13):
    total = 0
    for divisor, mu in zip(divisors, mobius):
        quotientResidue = residue13 * INVERSE_MOD_13[divisor % 13] % 13
        residue = divisor * quotientResidue
        total += mu * countResidueInInterval(low, high, 13 * divisor, residue)
    return total


def maxNegativeBranchA(limit):
    high = math.isqrt(limit) + 2
    low = 0
    while low + 1 < high:
        a = (low + high) // 2
        qMin = int(SQRT3 * a) + 1
        while qMin * qMin <= 3 * a * a:
            qMin += 1
        qMax = (5 * a - 1) // 2
        ok = qMin <= qMax and -(qMin * qMin - 5 * a * qMin + 3 * a * a) <= limit
        if ok:
            low = a
        else:
            high = a
    return low


def C(limit, spf):
    fourLimit = 4 * limit
    total = 0
    isqrt = math.isqrt

    pMax = isqrt(limit // 3)
    for p in range(1, pMax + 1):
        qMin = int(SQRT3 * p) + 1
        while qMin * qMin <= 3 * p * p:
            qMin += 1

        qMax = (isqrt(13 * p * p + fourLimit) - 5 * p) // 2
        while qMax >= qMin and qMax * qMax + 5 * p * qMax + 3 * p * p > limit:
            qMax -= 1
        if qMax < qMin:
            continue

        count, divisors, mobius = countCoprimeInterval(p, qMin, qMax, spf)
        if p % 13 != 0:
            count -= countCoprimeWithMod13(divisors, mobius, qMin, qMax, 4 * p % 13)
        total += count

    aMax = maxNegativeBranchA(limit)
    threshold = isqrt(fourLimit // 13)

    for a in range(1, aMax + 1):
        qMin = int(SQRT3 * a) + 1
        while qMin * qMin <= 3 * a * a:
            qMin += 1

        qMax = (5 * a - 1) // 2
        if qMax < qMin:
            continue

        if a > threshold:
            qMax = min(qMax, (5 * a - isqrt(13 * a * a - fourLimit)) // 2)
        while qMax >= qMin and -(qMax * qMax - 5 * a * qMax + 3 * a * a) > limit:
            qMax -= 1
        if qMax < qMin:
            continue

        count, divisors, mobius = countCoprimeInterval(a, qMin, qMax, spf)
        if a % 13 != 0:
            count -= countCoprimeWithMod13(divisors, mobius, qMin, qMax, (-4 * a) % 13)
        total += count

    return total


def bruteC(limit):
    count = 0
    squares = {z * z for z in range(1, limit + 1)}
    for x in range(1, limit + 1):
        for y in range(1, limit + 1):
            value = x * x + 5 * x * y + 3 * y * y
            if value > limit * limit:
                break
            if value in squares and math.gcd(x, y) == 1:
                count += 1
    return count


def solve():
    target = 10 ** 14
    maxP = max(math.isqrt(target // 3), maxNegativeBranchA(target))
    spf = smallestPrimeFactorSieve(maxP)
    return C(target, spf)


def runTests():
    spf = smallestPrimeFactorSieve(max(math.isqrt(10 ** 6 // 3), maxNegativeBranchA(10 ** 6)))
    assert bruteC(10 ** 3) == 142
    assert C(10 ** 3, spf) == 142
    assert C(10 ** 6, spf) == 142_463


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
