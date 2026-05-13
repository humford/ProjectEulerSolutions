import collections
import math
import time

import numpy as np


def divisorCountsSlow(limit):
    counts = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            counts[multiple] += 1
    return counts


def primeSieve(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit // 2 + 1)
    sieve[0] = 0

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number // 2]:
            start = number * number // 2
            sieve[start::number] = b"\x00" * ((len(sieve) - start - 1) // number + 1)

    primes = [2]
    primes.extend(2 * index + 1 for index in range(1, len(sieve)) if sieve[index])
    return primes


def divisorCountsSegment(start, stop, primes):
    values = np.arange(start, stop + 1, dtype=np.int64)
    counts = np.ones(stop - start + 1, dtype=np.uint16)

    for prime in primes:
        if prime * prime > stop:
            break

        offset = (-start) % prime
        remaining = values[offset::prime]
        divisorCounts = counts[offset::prime]

        divisorCounts *= 2
        remaining //= prime

        factor = 3
        while True:
            divisible = remaining % prime == 0
            if not divisible.any():
                break

            divisorCounts[divisible] = (divisorCounts[divisible] // (factor - 1)) * factor
            remaining[divisible] //= prime
            factor += 1

    counts[values > 1] *= 2
    return counts


def maxDivisorWindowSum(limit, window, segmentSize=1_000_000):
    primes = primeSieve(math.isqrt(limit))
    mostRecent = []
    total = 0

    for start in range(1, limit + 1, segmentSize):
        stop = min(limit, start + segmentSize - 1)
        divisorCounts = divisorCountsSegment(start, stop, primes)

        for offset, current in enumerate(divisorCounts.tolist()):
            index = start + offset
            if current >= len(mostRecent):
                mostRecent.extend([0] * (current + 1 - len(mostRecent)))
            mostRecent[current] = index

            tooFar = index - window
            while mostRecent and mostRecent[-1] <= tooFar:
                mostRecent.pop()

            if index >= window:
                total += len(mostRecent) - 1

    return total


def bruteMaxDivisorWindowSum(limit, window):
    divisorCounts = divisorCountsSlow(limit)
    queue = collections.deque()
    total = 0

    for index in range(1, limit + 1):
        while queue and divisorCounts[queue[-1]] <= divisorCounts[index]:
            queue.pop()
        queue.append(index)
        if queue[0] <= index - window:
            queue.popleft()
        if index >= window:
            total += divisorCounts[queue[0]]

    return total


def runTests():
    assert divisorCountsSegment(1, 10, primeSieve(10)).tolist() == [
        1, 2, 2, 3, 2, 4, 2, 4, 3, 4,
    ]
    assert maxDivisorWindowSum(100, 5, 25) == bruteMaxDivisorWindowSum(100, 5)
    assert maxDivisorWindowSum(1_000, 10, 200) == 17_176


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maxDivisorWindowSum(100_000_000, 100_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
