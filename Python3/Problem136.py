import math
import time


def primesBelow(limit):
    sieve = bytearray(b"\x01") * limit
    if limit > 0:
        sieve[0] = 0
    if limit > 1:
        sieve[1] = 0

    for n in range(2, math.isqrt(limit - 1) + 1):
        if sieve[n]:
            start = n * n
            sieve[start:limit:n] = b"\x00" * (((limit - 1 - start) // n) + 1)

    return [n for n in range(limit) if sieve[n]]


def singletonDifferenceCount(limit):
    primes = primesBelow(limit)
    return (
        sum(1 for prime in primes if prime % 4 == 3)
        + sum(1 for prime in primes if prime < limit // 4)
        + sum(1 for prime in primes if prime < limit // 16)
    )


def bruteSingletonDifferenceCount(limit):
    counts = [0] * limit

    for first_factor in range(1, int((3 * limit) ** 0.5) + 1):
        for second_factor in range(first_factor // 3 + 1, (limit - 1) // first_factor + 1):
            if (first_factor + second_factor) % 4 == 0:
                counts[first_factor * second_factor] += 1

    return counts.count(1)


def runTests():
    assert singletonDifferenceCount(1000) == bruteSingletonDifferenceCount(1000)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = singletonDifferenceCount(50000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
