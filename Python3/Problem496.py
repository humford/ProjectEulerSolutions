import math
import time


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))
    if limit >= 0:
        factors[0] = 0
    if limit >= 1:
        factors[1] = 1

    for value in range(2, math.isqrt(limit) + 1):
        if factors[value] == value:
            for multiple in range(value * value, limit + 1, value):
                if factors[multiple] == multiple:
                    factors[multiple] = value

    return factors


def squarefreeDivisorsWithMobiusTimesDivisor(n, smallestFactors):
    primeFactors = []
    remaining = n

    while remaining > 1:
        prime = smallestFactors[remaining]
        primeFactors.append(prime)
        while remaining % prime == 0:
            remaining //= prime

    divisors = [(1, 1)]
    for prime in primeFactors:
        current = divisors[:]
        for divisor, coefficient in current:
            divisors.append((divisor * prime, -coefficient * prime))

    return divisors


def coprimeSum(divisors, limit):
    if limit <= 0:
        return 0

    total = 0
    for divisor, coefficient in divisors:
        count = limit // divisor
        total += coefficient * count * (count + 1) // 2

    return total


def triangleCenterSum(limit):
    maxP = math.isqrt(limit) + 1
    smallestFactors = smallestPrimeFactors(maxP)
    divisorData = [None] * (maxP + 1)
    divisorData[1] = [(1, 1)]

    for p in range(2, maxP + 1):
        divisorData[p] = squarefreeDivisorsWithMobiusTimesDivisor(p, smallestFactors)

    total = 0
    for p in range(1, maxP + 1):
        lowQ = p + 1
        highQ = min(2 * p - 1, limit // p)
        if lowQ > highQ:
            continue

        quotientLimit = limit // p
        divisors = divisorData[p]
        q = lowQ

        while q <= highQ:
            quotient = quotientLimit // q
            lastQ = min(highQ, quotientLimit // quotient)
            sumQ = coprimeSum(divisors, lastQ) - coprimeSum(divisors, q - 1)

            if sumQ:
                total += p * quotient * (quotient + 1) // 2 * sumQ

            q = lastQ + 1

    return total


def runTests():
    assert triangleCenterSum(15) == 45


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangleCenterSum(10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
