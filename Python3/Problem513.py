import math
import time

import numpy


def bruteIntegralMedianCount(limit):
    total = 0
    for a in range(1, limit + 1):
        for b in range(a, limit + 1):
            for c in range(b, limit + 1):
                if a + b <= c:
                    continue

                medianSquaredTimesFour = 2 * a * a + 2 * b * b - c * c
                medianTwice = math.isqrt(medianSquaredTimesFour)
                if medianTwice * medianTwice == medianSquaredTimesFour and medianTwice % 2 == 0:
                    total += 1
    return total


def _firstAtParity(values, parity):
    return values + ((parity - values) & 1)


def integralMedianCount(limit):
    total = 0
    limitSquared = limit * limit

    # With c = 2d, u = (a+b)/2, and v = (b-a)/2, the median condition is
    # u^2 + v^2 = d^2 + m^2.  Factoring
    # (u-d)(u+d) = (m-v)(m+v) gives the coprime parametrisation
    # p = gA, q = hB, r = gB, s = hA, where gcd(A, B) = 1 and B > A.
    for aParam in range(1, limit // 2 + 1):
        xMin = (math.isqrt(limitSquared + 8 * aParam * aParam) - limit) // 2
        while xMin * xMin + limit * xMin < 2 * aParam * aParam:
            xMin += 1

        bStart = aParam + max(1, xMin)
        bStop = math.isqrt(aParam * (aParam + limit))
        if bStart > bStop:
            continue

        bParams = numpy.arange(bStart, bStop + 1, dtype=numpy.int64)
        coprime = numpy.gcd(bParams, aParam) == 1
        if not coprime.any():
            continue

        beforeSqrtThree = bParams * bParams < 3 * aParam * aParam
        lowerNumerator = numpy.where(beforeSqrtThree, 3 * aParam - bParams, bParams)
        lowerDenominator = numpy.where(beforeSqrtThree, bParams - aParam, aParam)

        denominator = bParams * lowerNumerator - aParam * lowerDenominator
        maxMultiplier = (limit * lowerDenominator) // denominator
        oddParams = (aParam % 2 == 1) & (bParams % 2 == 1)

        for gParam in range(1, int(maxMultiplier.max()) + 1):
            active = coprime & (maxMultiplier >= gParam)
            if not active.any():
                continue

            hMin = (gParam * lowerNumerator + lowerDenominator - 1) // lowerDenominator
            hMax = (limit + gParam * aParam) // bParams
            active &= hMin <= hMax
            if not active.any():
                continue

            if gParam % 2 == 1:
                active &= oddParams
                if not active.any():
                    continue
                firstH = _firstAtParity(hMin, 1)
            else:
                firstH = _firstAtParity(hMin, 0)

            counts = numpy.where(active & (firstH <= hMax), (hMax - firstH) // 2 + 1, 0)
            total += int(counts.sum())

    return total


def runTests():
    assert bruteIntegralMedianCount(10) == 3
    assert bruteIntegralMedianCount(20) == integralMedianCount(20)
    assert integralMedianCount(10) == 3
    assert integralMedianCount(50) == 165


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = integralMedianCount(100_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
