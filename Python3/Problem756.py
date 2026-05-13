import time
from array import array
from fractions import Fraction
from itertools import combinations
from math import comb


def totientSieve(limit):
    phi = array("I", [0]) * (limit + 1)
    primes = []
    if limit >= 1:
        phi[1] = 1

    for n in range(2, limit + 1):
        if phi[n] == 0:
            primes.append(n)
            phi[n] = n - 1
        for prime in primes:
            composite = n * prime
            if composite > limit:
                break
            if n % prime == 0:
                phi[composite] = phi[n] * prime
                break
            phi[composite] = phi[n] * (prime - 1)
    return phi


def expectedErrorByWeights(values, n, m):
    denominator = comb(n, m)
    total = Fraction(0, 1)
    for k in range(1, n - m + 1):
        total += Fraction(values[k] * comb(n - k, m), denominator)
    return total


def bruteExpectedError(values, n, m):
    total = Fraction(0, 1)
    sampleCount = 0
    exactSum = sum(values[1:])

    for sample in combinations(range(1, n + 1), m):
        previous = 0
        approximation = 0
        for selected in sample:
            approximation += values[selected] * (selected - previous)
            previous = selected
        total += exactSum - approximation
        sampleCount += 1

    return total / sampleCount


def expectedErrorForLinear(n, m):
    values = [0] + list(range(1, n + 1))
    return expectedErrorByWeights(values, n, m)


def kahanAdd(total, compensation, value):
    adjusted = value - compensation
    updated = total + adjusted
    compensation = (updated - total) - adjusted
    return updated, compensation


def cutoffIndex(n, m, epsilon=1e-8):
    limit = n - m
    if limit <= 0:
        return 0

    weight = (n - m) / n
    for k in range(1, limit + 1):
        remaining = limit - k
        if remaining == 0:
            return k

        nMinusK = n - k
        nextWeight = weight * (nMinusK - m) / nMinusK
        if n * remaining * nextWeight < epsilon:
            return k
        weight = nextWeight

    return limit


def expectedErrorForTotient(n, m, truncate=True, epsilon=1e-8):
    limit = n - m
    if limit <= 0:
        return 0.0

    upto = cutoffIndex(n, m, epsilon) if truncate else limit
    phi = totientSieve(upto)

    weight = (n - m) / n
    total = 0.0
    compensation = 0.0
    for k in range(1, upto + 1):
        total, compensation = kahanAdd(total, compensation, phi[k] * weight)
        nMinusK = n - k
        if nMinusK <= m:
            break
        weight *= (nMinusK - m) / nMinusK

    return total


def runTests():
    values = [0, 5, 2, 7, 11, 3, 13]
    assert bruteExpectedError(values, 6, 3) == expectedErrorByWeights(values, 6, 3)

    assert expectedErrorForLinear(100, 50) == Fraction(2525, 1326)

    example = expectedErrorForTotient(10_000, 100, truncate=False)
    assert format(example, ".6f") == "5842.849907"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedErrorForTotient(12_345_678, 12_345)
    elapsed = time.time() - start

    print("Found " + format(answer, ".6f") + " in " + str(elapsed) + " seconds.")
