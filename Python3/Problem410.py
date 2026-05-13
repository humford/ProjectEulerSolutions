import time


def sameParityPairCount(leftLimit, rightLimit):
    leftOdd = (leftLimit + 1) // 2
    rightOdd = (rightLimit + 1) // 2
    leftEven = leftLimit // 2
    rightEven = rightLimit // 2
    return leftOdd * rightOdd + leftEven * rightEven


def distinctPrimeFactorCounts(limit):
    factorCounts = bytearray(limit + 1)

    for prime in range(2, limit + 1):
        if factorCounts[prime] == 0:
            for multiple in range(prime, limit + 1, prime):
                factorCounts[multiple] += 1

    return factorCounts


def tangentQuadrupletCount(radiusLimit, xLimit):
    limit = min(radiusLimit, xLimit)
    factorCounts = distinctPrimeFactorCounts(limit)

    total = 2 * radiusLimit * xLimit
    primitiveContribution = 0

    for legParameter in range(2, limit + 1):
        weight = 1 << (factorCounts[legParameter] - 1)
        radiusQuotient = radiusLimit // legParameter
        xQuotient = xLimit // legParameter

        if legParameter & 1:
            primitiveContribution += weight * radiusQuotient * xQuotient
        else:
            primitiveContribution += weight * sameParityPairCount(
                radiusQuotient,
                xQuotient,
            )

    return total + 4 * primitiveContribution


def answer():
    return 2 * tangentQuadrupletCount(10**8, 10**9)


def runTests():
    assert tangentQuadrupletCount(1, 5) == 10
    assert tangentQuadrupletCount(2, 10) == 52
    assert tangentQuadrupletCount(10, 100) == 3384


if __name__ == "__main__":
    runTests()
    start = time.time()
    print("Found", answer(), "in", time.time() - start, "seconds.")
