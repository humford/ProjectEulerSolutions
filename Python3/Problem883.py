from math import gcd, isqrt
import time


TARGET_R = 10**6


def chi3Prefix(limit):
    return (limit + 2) // 3 - (limit + 1) // 3


def latticePointCount(bound, cache):
    if bound <= 0:
        return 1
    if bound in cache:
        return cache[bound]

    total = 0
    index = 1
    while index <= bound:
        quotient = bound // index
        end = bound // quotient
        total += quotient * (chi3Prefix(end) - chi3Prefix(index - 1))
        index = end + 1

    count = 1 + 6 * total
    cache[bound] = count
    return count


def distinctPrimeFactorCounts(limit):
    counts = [0] * (limit + 1)

    for value in range(2, limit + 1):
        if counts[value] != 0:
            continue
        for multiple in range(value, limit + 1, value):
            counts[multiple] += 1

    return counts


def shapeMultiplicities(maxD):
    multiplicities = [0] * (maxD + 1)

    firstLimit = maxD // 3
    omega = distinctPrimeFactorCounts(firstLimit)
    for product in range(2, firstLimit + 1):
        if product % 3 != 1:
            multiplicities[3 * product] += 1 << (omega[product] - 1)

    for v in range(1, maxD // 3 + 1):
        maxA = (isqrt(9 * v * v + 4 * maxD) - 3 * v) // 2
        for a in range(1, maxA + 1):
            u = v + a
            if u % 3 == v % 3:
                continue
            if gcd(u, v) != 1:
                continue
            multiplicities[a * (a + 3 * v)] += 1

    return multiplicities


def T(radiusNumerator, radiusDenominator=1):
    maxD = isqrt(
        12 * radiusNumerator * radiusNumerator
        // (radiusDenominator * radiusDenominator)
    )
    multiplicities = shapeMultiplicities(maxD)
    pointCountCache = {}

    scaledNumerator = 12 * radiusNumerator * radiusNumerator
    scaledDenominator = radiusDenominator * radiusDenominator

    scalene = 0
    for d, multiplicity in enumerate(multiplicities):
        if multiplicity == 0:
            continue

        bound = scaledNumerator // (scaledDenominator * d * d)
        if d % 3 != 0:
            bound //= 3

        directions = latticePointCount(bound, pointCountCache) - 1
        scalene += 2 * multiplicity * directions

    equilateralBound = (
        4 * radiusNumerator * radiusNumerator
        // (radiusDenominator * radiusDenominator)
    )
    equilateral = (latticePointCount(equilateralBound, pointCountCache) - 1) // 3

    return scalene + equilateral


def solve():
    return T(TARGET_R)


def runTests():
    assert T(1, 2) == 2
    assert T(2) == 44
    assert T(10) == 1302
    assert solve() == 14854003484704


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
