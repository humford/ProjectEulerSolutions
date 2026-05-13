import math
import time


LIMIT = 5 * 10**15


def primeSieve(limit):
    if limit < 2:
        return bytearray(limit + 1)

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    if limit >= 4:
        sieve[4 : limit + 1 : 2] = b"\x00" * ((limit - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start : limit + 1 : step] = b"\x00" * (
                (limit - start) // step + 1
            )

    return sieve


def sqrtMinusOneModPrime(prime):
    candidate = 2
    half = (prime - 1) // 2

    while pow(candidate, half, prime) != prime - 1:
        candidate += 1

    return pow(candidate, (prime - 1) // 4, prime)


def panaitopolPrimeCount(limit):
    max_n = (math.isqrt(2 * limit - 1) - 1) // 2

    while 2 * max_n * max_n + 2 * max_n + 1 >= limit:
        max_n -= 1
    while 2 * (max_n + 1) * (max_n + 1) + 2 * (max_n + 1) + 1 < limit:
        max_n += 1

    candidates = bytearray(b"\x01") * (max_n + 1)
    candidates[0] = 0
    primes = primeSieve(math.isqrt(limit - 1))

    for prime in range(5, len(primes), 4):
        if primes[prime] == 0:
            continue

        root = sqrtMinusOneModPrime(prime)
        inverse_two = (prime + 1) // 2

        for residue in (
            (root - 1) * inverse_two % prime,
            (prime - root - 1) * inverse_two % prime,
        ):
            start = residue
            if start < 1:
                start += prime
            if 2 * start * start + 2 * start + 1 == prime:
                start += prime

            if start <= max_n:
                candidates[start : max_n + 1 : prime] = b"\x00" * (
                    (max_n - start) // prime + 1
                )

    return sum(candidates)


def runTests():
    assert panaitopolPrimeCount(1000) == 10


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = panaitopolPrimeCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
