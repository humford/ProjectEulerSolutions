import math
import time


def smallestPrimeFactorSieve(limit):
    smallestPrimeFactor = list(range(limit + 1))
    for n in range(2, math.isqrt(limit) + 1):
        if smallestPrimeFactor[n] == n:
            for multiple in range(n * n, limit + 1, n):
                if smallestPrimeFactor[multiple] == multiple:
                    smallestPrimeFactor[multiple] = n
    return smallestPrimeFactor


def distinctPrimeFactors(n, smallestPrimeFactor):
    factors = []
    while n > 1:
        prime = smallestPrimeFactor[n]
        factors.append(prime)
        while n % prime == 0:
            n //= prime
    return factors


def S(N):
    maxA = math.isqrt(N // 3)
    smallestPrimeFactor = smallestPrimeFactorSieve(maxA)
    total = 0

    for a in range(1, maxA + 1):
        aSquared = a * a
        primeFactors = distinctPrimeFactors(a, smallestPrimeFactor)

        if 5 * aSquared <= N:
            minB = 1
        else:
            minB = (5 * aSquared - N + 2 * a - 1) // (2 * a)
            minB = max(minB, 1)

        # Positivity of 3a^2 - 8ab + 5b^2 in the needed branch.
        maxB = (3 * a - 1) // 5
        if maxB < minB:
            continue

        discA = 4 * aSquared + 12 * N
        maxBForA = (-2 * a + math.isqrt(discA)) // 6

        discC = aSquared + 5 * N
        sqrtDiscC = math.isqrt(discC)
        minBForC = (4 * a - sqrtDiscC + 4) // 5
        maxBForC = (4 * a + sqrtDiscC) // 5

        minB = max(minB, minBForC)
        maxB = min(maxB, maxBForA, maxBForC, a - 1)
        if maxB < minB:
            continue

        for b in range(minB, maxB + 1):
            if any(b % prime == 0 for prime in primeFactors):
                continue

            ab = a * b
            bSquared = b * b

            x = 2 * ab + 3 * bSquared
            y = 5 * aSquared - 2 * ab
            z = 3 * aSquared - 8 * ab + 5 * bSquared

            if z <= 0 or x > N or y > N or z > N:
                continue

            if x % 19 == 0 and y % 19 == 0:
                continue

            total += 8 * (aSquared - ab + bSquared)

    return total


def runTests():
    assert S(10 ** 2) == 184


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
