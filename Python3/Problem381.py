import math
import time


LIMIT = 10**8


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


def factorialTailResidue(prime):
    return ((prime - 3) * pow(8, -1, prime)) % prime


def factorialTailSum(limit=LIMIT):
    primes = primeSieve(limit)
    return sum(factorialTailResidue(prime) for prime in range(5, limit) if primes[prime])


def runTests():
    assert factorialTailResidue(7) == 4
    assert factorialTailSum(100) == 480


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = factorialTailSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
