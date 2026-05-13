import math
import time


LIMIT = 10**6


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    sieve[0] = 0
    sieve[1] = 0

    if limit > 4:
        sieve[4::2] = b"\x00" * ((limit - 1 - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit - 1) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start::step] = b"\x00" * ((limit - 1 - start) // step + 1)

    return sieve


def slidingGameSquareCount(limit):
    primes = primeSieve(limit)
    total = 0

    for prime in range(2, limit):
        if primes[prime]:
            total += 2 if prime == 3 else (prime * prime - 1) // 12

    return total


def runTests():
    assert slidingGameSquareCount(100) == 5482


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = slidingGameSquareCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
