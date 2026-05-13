import math
import time


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for n in range(2, math.isqrt(limit) + 1):
        if sieve[n]:
            start = n * n
            sieve[start: limit + 1: n] = b"\x00" * ((limit - start) // n + 1)

    return sieve


def F(n):
    return (7 * n + 15) / (18 * (n + 1))


def averageForOddPrimesBelow(limit):
    isPrime = primeSieve(limit - 1)
    total = 0.0
    count = 0

    for n in range(3, limit, 2):
        if isPrime[n]:
            total += F(n)
            count += 1

    return total / count


def formattedAverage(limit):
    return f"{averageForOddPrimesBelow(limit):.10f}"


def runTests():
    assert F(3) == 0.5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedAverage(10 ** 6)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
