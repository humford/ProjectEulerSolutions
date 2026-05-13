import math
import time


LIMIT = 10_000_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    if limit >= 4:
        sieve[4::2] = b"\x00" * ((limit - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start::step] = b"\x00" * ((limit - start) // step + 1)

    return [2] + [number for number in range(3, limit + 1, 2) if sieve[number]]


def largestTwoPrimeMultiple(prime1, prime2, limit):
    best = 0
    power1 = prime1

    while power1 * prime2 <= limit:
        power2 = prime2

        while power1 * power2 <= limit:
            best = max(best, power1 * power2)
            power2 *= prime2

        power1 *= prime1

    return best


def twoPrimeMultipleSum(limit=LIMIT):
    primes = primeSieve(limit // 2)
    total = 0

    for index, prime1 in enumerate(primes):
        if prime1 * prime1 > limit:
            break

        maxPrime2 = limit // prime1
        nextIndex = index + 1

        while nextIndex < len(primes) and primes[nextIndex] <= maxPrime2:
            total += largestTwoPrimeMultiple(prime1, primes[nextIndex], limit)
            nextIndex += 1

    return total


def runTests():
    assert largestTwoPrimeMultiple(2, 3, 100) == 96
    assert largestTwoPrimeMultiple(3, 5, 100) == 75
    assert largestTwoPrimeMultiple(2, 73, 100) == 0
    assert twoPrimeMultipleSum(100) == 2262


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = twoPrimeMultipleSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
