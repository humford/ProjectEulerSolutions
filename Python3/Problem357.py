import math
import time


LIMIT = 100_000_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 2)
    sieve[0] = 0
    sieve[1] = 0

    for number in range(4, limit + 1, 2):
        sieve[number] = 0

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start : limit + 1 : step] = b"\x00" * ((limit - start) // step + 1)

    return sieve


def isPrimeGenerating(number, primes):
    for divisor in range(2, math.isqrt(number) + 1):
        if number % divisor == 0 and not primes[divisor + number // divisor]:
            return False

    return True


def primeGeneratingIntegerSum(limit=LIMIT):
    primes = primeSieve(limit + 1)
    total = 1

    for prime in range(3, limit + 2, 2):
        if primes[prime]:
            number = prime - 1

            if isPrimeGenerating(number, primes):
                total += number

    return total


def runTests():
    assert isPrimeGenerating(30, primeSieve(31))
    assert primeGeneratingIntegerSum(100) == 401


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeGeneratingIntegerSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
