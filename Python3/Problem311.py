import time
from bisect import bisect_left, bisect_right
from collections import defaultdict
from functools import lru_cache
from math import isqrt


LIMIT = 10_000_000_000


def choose2(number):
    return number * (number - 1) // 2


def choose3(number):
    return number * (number - 1) * (number - 2) // 6


def oddPrimeSieve(limit):
    sieve = bytearray(b"\x01") * (limit // 2 + 1)

    if sieve:
        sieve[0] = 0

    for prime in range(3, isqrt(limit) + 1, 2):
        if sieve[prime // 2]:
            start = prime * prime // 2
            sieve[start::prime] = b"\x00" * (((len(sieve) - 1 - start) // prime) + 1)

    return sieve


def oneModFourPrimes(limit, primeSieve):
    if limit < 5:
        return []

    return [prime for prime in range(5, limit + 1, 4) if primeSieve[prime // 2]]


def threeModFourSmoothPrefix(limit, primeSieve):
    smooth = bytearray(limit + 1)

    if limit >= 1:
        smooth[1] = 1

    for prime in range(3, limit + 1, 4):
        if not primeSieve[prime // 2]:
            continue

        base = 1
        while base <= limit // prime:
            if smooth[base]:
                value = base * prime
                while value <= limit:
                    smooth[value] = 1
                    value *= prime
            base += 2

    prefix = [0] * (limit + 1)
    total = 0

    for number in range(1, limit + 1):
        total += smooth[number]
        prefix[number] = total

    return prefix


def strictContainmentCount(intervals):
    if len(intervals) < 2:
        return 0

    intervals.sort(key=lambda interval: (interval[0], -interval[1]))
    rightValues = sorted({right for _left, right in intervals})
    fenwick = [0] * (len(rightValues) + 1)

    def add(index):
        while index < len(fenwick):
            fenwick[index] += 1
            index += index & -index

    def prefixSum(index):
        total = 0

        while index:
            total += fenwick[index]
            index -= index & -index

        return total

    total = 0
    index = 0

    while index < len(intervals):
        left = intervals[index][0]
        nextIndex = index

        while nextIndex < len(intervals) and intervals[nextIndex][0] == left:
            nextIndex += 1

        previousTotal = prefixSum(len(rightValues))
        for _left, right in intervals[index:nextIndex]:
            position = bisect_left(rightValues, right) + 1
            total += previousTotal - prefixSum(position)

        for _left, right in intervals[index:nextIndex]:
            position = bisect_left(rightValues, right) + 1
            add(position)

        index = nextIndex

    return total


def bruteBiclinicCount(limit):
    keyLimit = limit // 4
    radiusLimit = isqrt(keyLimit)
    squares = [number * number for number in range(radiusLimit + 1)]
    representations = defaultdict(list)

    for u in range(1, radiusLimit + 1):
        uSquared = squares[u]

        for v in range(u + 1):
            key = uSquared + squares[v]
            if key > keyLimit:
                break

            representations[key].append((u, v))

    total = 0

    for s in range(1, radiusLimit + 1):
        sSquared = squares[s]
        rLimit = min(s, isqrt(keyLimit - sSquared))

        for r in range(1, rLimit + 1):
            intervals = []

            for u, v in representations.get(sSquared + squares[r], ()):
                if v > 0 and v < s < u:
                    intervals.append((u - v, u + v))

            total += strictContainmentCount(intervals)

    return total


def biclinicCount(limit):
    # For a fixed key m = BO^2 + AO^2, each positive representation
    # m = u^2 + v^2 gives the side interval [u - v, u + v].  As v increases
    # these intervals strictly nest, so the geometry count is determined only
    # by the number of sum-of-two-squares representations of m.
    keyLimit = limit // 4

    if keyLimit < 325:
        return 0

    onePrimeLimit = keyLimit // 25
    multiplierLimit = keyLimit // 325
    smoothLimit = isqrt(multiplierLimit)
    primeSieve = oddPrimeSieve(max(onePrimeLimit, smoothLimit))
    primes = oneModFourPrimes(onePrimeLimit, primeSieve)
    smoothPrefix = threeModFourSmoothPrefix(smoothLimit, primeSieve)

    @lru_cache(maxsize=None)
    def neutralMultiplierCounts(maximum):
        evenTwoPowerCount = 0
        oddTwoPowerCount = 0
        powerOfTwo = 1
        isOddPower = False

        while powerOfTwo <= maximum:
            count = smoothPrefix[isqrt(maximum // powerOfTwo)]

            if isOddPower:
                oddTwoPowerCount += count
            else:
                evenTwoPowerCount += count

            powerOfTwo *= 2
            isOddPower = not isOddPower

        return evenTwoPowerCount, oddTwoPowerCount

    @lru_cache(maxsize=None)
    def minimumMultiplierToReach(divisorChoices, startIndex):
        if divisorChoices >= 5:
            return 1

        best = keyLimit + 1

        for index in range(startIndex, min(startIndex + 5, len(primes))):
            prime = primes[index]
            primePower = prime

            for exponent in range(1, 5):
                candidate = primePower * minimumMultiplierToReach(
                    divisorChoices * (exponent + 1),
                    index + 1,
                )

                if candidate < best:
                    best = candidate

                primePower *= prime

        return best

    total = 0

    def addCoreContribution(core, divisorChoices, isSquare):
        evenTwoPowers, oddTwoPowers = neutralMultiplierCounts(keyLimit // core)

        if isSquare:
            representationCount = (divisorChoices - 1) // 2
            return (
                evenTwoPowers * choose3(representationCount)
                + oddTwoPowers
                * (choose3(representationCount) + choose2(representationCount))
            )

        representationCount = divisorChoices // 2
        return (evenTwoPowers + oddTwoPowers) * choose3(representationCount)

    def searchCores(startIndex, core, divisorChoices, isSquare):
        nonlocal total

        if divisorChoices >= 5:
            total += addCoreContribution(core, divisorChoices, isSquare)

        maxPrime = keyLimit // core
        endIndex = bisect_right(primes, maxPrime, lo=startIndex)

        for index in range(startIndex, endIndex):
            prime = primes[index]
            nextCore = core * prime
            exponent = 1

            while nextCore <= keyLimit:
                nextDivisorChoices = divisorChoices * (exponent + 1)

                if (
                    nextCore
                    * minimumMultiplierToReach(nextDivisorChoices, index + 1)
                    <= keyLimit
                ):
                    searchCores(
                        index + 1,
                        nextCore,
                        nextDivisorChoices,
                        isSquare and exponent % 2 == 0,
                    )

                exponent += 1
                nextCore *= prime

    searchCores(0, 1, 1, True)

    return total


def runTests():
    for limit in (10_000, 100_000):
        assert biclinicCount(limit) == bruteBiclinicCount(limit)

    assert biclinicCount(10_000) == 49
    assert biclinicCount(1_000_000) == 38239


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = biclinicCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
