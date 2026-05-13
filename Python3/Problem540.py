from array import array
from math import isqrt
import time


def oddSmallestPrimeFactors(limit):
    factors = array("I", [0]) * (limit // 2 + 1)
    factors[0] = 1
    root = isqrt(limit)

    for p in range(3, root + 1, 2):
        if factors[p // 2] != 0:
            continue

        factors[p // 2] = p
        for index in range((p * p) // 2, len(factors), p):
            if factors[index] == 0:
                factors[index] = p

    return factors


def distinctFactorsAndTotient(n, smallestPrimeFactors):
    factors = []
    totient = n
    remaining = n

    while remaining > 1:
        p = smallestPrimeFactors[remaining // 2]
        if p == 0:
            p = remaining

        factors.append(p)
        totient = totient // p * (p - 1)
        while remaining % p == 0:
            remaining //= p

    return factors, totient


def boundedOddCoprimeCount(limit, factors):
    total = (limit + 1) // 2

    def includeProducts(start, product, sign):
        nonlocal total
        for index in range(start, len(factors)):
            nextProduct = product * factors[index]
            total += sign * ((limit // nextProduct + 1) // 2)
            if nextProduct <= limit:
                includeProducts(index + 1, nextProduct, -sign)

    includeProducts(0, 1, -1)
    return total


def primitiveTripleCount(limit):
    maxOddParameter = isqrt(2 * limit - 1)
    fullTotientLimit = isqrt(limit)
    smallestPrimeFactors = oddSmallestPrimeFactors(maxOddParameter)

    total = 0
    for m in range(3, maxOddParameter + 1, 2):
        factors, totient = distinctFactorsAndTotient(m, smallestPrimeFactors)

        if m <= fullTotientLimit:
            total += totient // 2
        else:
            xLimit = isqrt(2 * limit - m * m)
            total += boundedOddCoprimeCount(xLimit, factors)

    return total


def runTests():
    assert primitiveTripleCount(20) == 3
    assert primitiveTripleCount(10 ** 6) == 159_139


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primitiveTripleCount(3_141_592_653_589_793)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
