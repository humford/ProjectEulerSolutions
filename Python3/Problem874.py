from heapq import heappop, heappush
import time


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, int(limit**0.5) + 1):
        if isPrime[n]:
            start = n * n
            isPrime[start:limit + 1:n] = b"\x00" * (((limit - start) // n) + 1)

    return [n for n in range(limit + 1) if isPrime[n]]


def firstPrimes(count):
    limit = 20
    while True:
        primes = primeSieve(limit)
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def minimumAdjustmentLoss(k, n, primes):
    topPrime = primes[k - 1]
    losses = [0] + [topPrime - primes[k - 1 - reduction] for reduction in range(1, k)]
    target = (-n) % k

    distances = [10**30] * k
    distances[0] = 0
    queue = [(0, 0)]

    while queue:
        distance, residue = heappop(queue)
        if distance != distances[residue]:
            continue
        if residue == target:
            return distance

        for reduction in range(1, k):
            nextResidue = residue + reduction
            if nextResidue >= k:
                nextResidue -= k

            newDistance = distance + losses[reduction]
            if newDistance < distances[nextResidue]:
                distances[nextResidue] = newDistance
                heappush(queue, (newDistance, nextResidue))

    return distances[target]


def M(k, n):
    primes = firstPrimes(k + 1)
    baseScore = n * primes[k - 1]
    return baseScore - minimumAdjustmentLoss(k, n, primes)


def runTests():
    assert M(2, 5) == 14


def solve():
    primes = firstPrimes(7001)
    n = primes[7000]
    return n * primes[6999] - minimumAdjustmentLoss(7000, n, primes)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
