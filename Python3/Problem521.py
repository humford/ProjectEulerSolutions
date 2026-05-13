import math
import sys
import time


MODULUS = 10 ** 9
SMALL_PRIME_LIMIT = 5_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0

    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)

    return [number for number in range(limit + 1) if sieve[number]]


def triangleSumFromTwo(limit):
    return (limit * (limit + 1) // 2 - 1) % MODULUS


def primeSumMod(limit, primes):
    values = []
    index = 1
    while index <= limit:
        value = limit // index
        values.append(value)
        index = limit // value + 1
    values.sort()

    sums = {value: triangleSumFromTwo(value) for value in values}
    previousPrimeSum = 0

    # This is the standard distinct-quotient prime-sum sieve.  sums[x] starts
    # as sum(2..x), and each prime removes composites whose least remaining
    # prime factor is that prime.
    for prime in primes:
        square = prime * prime
        if square > limit:
            break

        currentPrimeSum = sums[prime]
        if currentPrimeSum == previousPrimeSum:
            continue

        for valueIndex in range(len(values) - 1, -1, -1):
            value = values[valueIndex]
            if value < square:
                break
            sums[value] -= prime * (sums[value // prime] - previousPrimeSum)
            sums[value] %= MODULUS

        previousPrimeSum = currentPrimeSum

    return sums[limit]


def roughCountMod(limit, excludedPrimeCount, primes, cache):
    if excludedPrimeCount == 0:
        return limit % MODULUS
    if limit == 0:
        return 0

    key = None
    if limit < SMALL_PRIME_LIMIT:
        key = (limit, excludedPrimeCount)
        if key in cache:
            return cache[key]

    result = roughCountMod(limit, excludedPrimeCount - 1, primes, cache)
    result -= roughCountMod(limit // primes[excludedPrimeCount - 1], excludedPrimeCount - 1, primes, cache)
    result %= MODULUS

    if key is not None:
        cache[key] = result
    return result


def compositeSmallestPrimeFactorSum(limit, primes):
    splitIndex = 0
    while splitIndex < len(primes) and primes[splitIndex] < SMALL_PRIME_LIMIT:
        splitIndex += 1
    smallPrimeCount = splitIndex + (1 if splitIndex < len(primes) else 0)

    cache = {}
    total = 0
    for index in range(smallPrimeCount):
        prime = primes[index]
        count = roughCountMod(limit // prime, index, primes, cache) - 1
        total += prime * count
        total %= MODULUS

    if smallPrimeCount >= len(primes):
        return total

    bound = limit // primes[smallPrimeCount - 1]
    marked = bytearray(bound + 1)
    if bound >= 1:
        marked[1] = 1

    for prime in primes[:smallPrimeCount]:
        marked[prime : bound + 1 : prime] = b"\x01" * (((bound - prime) // prime) + 1)

    remaining = sum(1 for number in range(2, bound + 1) if not marked[number])
    previousBound = bound

    for index in range(smallPrimeCount, len(primes)):
        prime = primes[index]
        currentBound = limit // prime

        for number in range(previousBound, currentBound, -1):
            if not marked[number]:
                remaining -= 1

        total += prime * remaining
        total %= MODULUS

        for number in range(prime, currentBound + 1, prime):
            if not marked[number]:
                marked[number] = 1
                remaining -= 1

        previousBound = currentBound

    return total


def smallestPrimeFactorSum(limit):
    primes = primeSieve(math.isqrt(limit))
    primeContribution = primeSumMod(limit, primes)
    compositeContribution = compositeSmallestPrimeFactorSum(limit, primes)
    return (primeContribution + compositeContribution) % MODULUS


def bruteSmallestPrimeFactorSum(limit):
    smallest = list(range(limit + 1))
    for prime in range(2, math.isqrt(limit) + 1):
        if smallest[prime] == prime:
            for multiple in range(prime * prime, limit + 1, prime):
                if smallest[multiple] == multiple:
                    smallest[multiple] = prime
    return sum(smallest[2:]) % MODULUS


def runTests():
    assert smallestPrimeFactorSum(100) == 1_257
    assert smallestPrimeFactorSum(1_000) == bruteSmallestPrimeFactorSum(1_000)


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    runTests()
    start = time.time()
    answer = smallestPrimeFactorSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
