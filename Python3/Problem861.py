import math
import sys
import time


TARGET_N = 10**12


def sieveWithPi(limit):
    if limit < 2:
        return [], [0] * (limit + 1)

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, math.isqrt(limit) + 1):
        if isPrime[n]:
            start = n * n
            isPrime[start:limit + 1:n] = b"\x00" * (((limit - start) // n) + 1)

    primes = [n for n in range(2, limit + 1) if isPrime[n]]
    pi = [0] * (limit + 1)
    count = 0
    for n in range(limit + 1):
        if isPrime[n]:
            count += 1
        pi[n] = count

    return primes, pi


def buildPrimePiTable(limit, primes, root):
    if limit // root == root:
        smallStart = root - 1
    else:
        smallStart = root

    length = root + smallStart
    counts = [0] * length

    for i in range(root):
        counts[i] = limit // (i + 1) - 1

    for value in range(1, smallStart + 1):
        counts[length - value] = value - 1

    for prime in primes:
        primeSquare = prime * prime
        if primeSquare > limit:
            break

        smallPrimeCount = counts[length - (prime - 1)]

        if primeSquare <= root:
            divisor = prime
            for i in range(root):
                if divisor <= root:
                    counts[i] -= counts[divisor - 1] - smallPrimeCount
                else:
                    counts[i] -= counts[length - (limit // divisor)] - smallPrimeCount
                divisor += prime

            if primeSquare <= smallStart:
                for value in range(smallStart, primeSquare - 1, -1):
                    counts[length - value] -= (
                        counts[length - (value // prime)] - smallPrimeCount
                    )
        else:
            end = min(limit // primeSquare, root)
            divisor = prime
            for i in range(end):
                if divisor <= root:
                    counts[i] -= counts[divisor - 1] - smallPrimeCount
                else:
                    counts[i] -= counts[length - (limit // divisor)] - smallPrimeCount
                divisor += prime

    return counts


def computeQs(limit):
    root = math.isqrt(limit)
    primes, piSmall = sieveWithPi(root)
    primeCounts = buildPrimePiTable(limit, primes, root)
    tableLength = len(primeCounts)
    primeCount = len(primes)

    def primePi(n):
        if n <= root:
            return piSmall[n]
        return primeCounts[limit // n - 1]

    sys.setrecursionlimit(1_000_000)

    def countSquarefree(limitPart, primesLeft, startIndex, forbidden):
        if primesLeft == 0:
            return 1
        if startIndex >= primeCount:
            return 0

        if primesLeft == 1:
            if limitPart < primes[startIndex]:
                return 0

            total = primePi(limitPart)
            if startIndex > 0:
                total -= piSmall[primes[startIndex - 1]]

            startPrime = primes[startIndex]
            for prime in forbidden:
                if startPrime <= prime <= limitPart:
                    total -= 1
            return total

        if primesLeft == 2:
            total = 0
            for i in range(startIndex, primeCount):
                prime = primes[i]
                if prime * prime > limitPart:
                    break
                if prime in forbidden:
                    continue

                upper = limitPart // prime
                subtotal = primePi(upper) - piSmall[prime]
                for forbiddenPrime in forbidden:
                    if prime < forbiddenPrime <= upper:
                        subtotal -= 1
                total += subtotal
            return total

        if primesLeft == 3:
            total = 0
            for i in range(startIndex, primeCount):
                prime = primes[i]
                if prime * prime * prime > limitPart:
                    break
                if prime in forbidden:
                    continue
                total += countSquarefree(limitPart // prime, 2, i + 1, forbidden)
            return total

        if primesLeft == 4:
            total = 0
            for i in range(startIndex, primeCount):
                prime = primes[i]
                if prime * prime * prime * prime > limitPart:
                    break
                if prime in forbidden:
                    continue
                total += countSquarefree(limitPart // prime, 3, i + 1, forbidden)
            return total

        raise ValueError("Too many squarefree primes requested")

    qValues = [0] * 11

    def addPowerfulPart(powerfulPart, divisorCount, primesUsed):
        remaining = limit // powerfulPart

        for squarefreePrimes in range(5):
            biUnitaryDivisors = divisorCount << squarefreePrimes
            if biUnitaryDivisors > 20:
                break
            if biUnitaryDivisors >= 4:
                k = biUnitaryDivisors // 2
                if 2 <= k <= 10:
                    qValues[k] += countSquarefree(
                        remaining,
                        squarefreePrimes,
                        0,
                        primesUsed,
                    )

    def searchPowerfulParts(startIndex, powerfulPart, divisorCount, primesUsed):
        addPowerfulPart(powerfulPart, divisorCount, primesUsed)

        for i in range(startIndex, primeCount):
            prime = primes[i]
            if powerfulPart * prime * prime > limit:
                break

            exponent = 2
            primePower = prime * prime
            remaining = limit // powerfulPart

            while exponent <= 20 and primePower <= remaining:
                factor = exponent if exponent % 2 == 0 else exponent + 1
                newDivisorCount = divisorCount * factor
                if newDivisorCount <= 20:
                    searchPowerfulParts(
                        i + 1,
                        powerfulPart * primePower,
                        newDivisorCount,
                        primesUsed + (prime,),
                    )

                exponent += 1
                primePower *= prime

    searchPowerfulParts(0, 1, 1, ())
    return qValues


def solve(limit=TARGET_N):
    qValues = computeQs(limit)
    return sum(qValues[2:11])


def runTests():
    q100 = computeQs(10**2)
    assert q100[2] == 51

    qMillion = computeQs(10**6)
    assert qMillion[6] == 6189


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
