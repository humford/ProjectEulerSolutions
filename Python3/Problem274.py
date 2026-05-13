import math
import time


LIMIT = 10**7


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    sieve[0] = 0
    sieve[1] = 0

    if limit > 4:
        sieve[4::2] = b"\x00" * ((limit - 1 - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit - 1) + 1, 2):
        if sieve[number]:
            sieve[number * number :: 2 * number] = b"\x00" * (
                (limit - 1 - number * number) // (2 * number) + 1
            )

    return sieve


def divisibilityMultiplier(prime):
    return pow(10, -1, prime)


def divisibilityMultiplierSum(limit):
    primes = primeSieve(limit)
    total = 0

    for prime in range(3, limit, 2):
        if prime != 5 and primes[prime]:
            total += divisibilityMultiplier(prime)

    return total


def runTests():
    assert divisibilityMultiplier(113) == 34
    assert divisibilityMultiplierSum(1000) == 39517


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisibilityMultiplierSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
