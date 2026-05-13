import math
import time


PREFIX = 137
SUFFIX = 56789
SUFFIX_MODULUS = 100000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    for number in range(4, limit + 1, 2):
        sieve[number] = 0

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start::step] = b"\x00" * ((limit - start) // step + 1)

    return [2] + [number for number in range(3, limit + 1, 2) if sieve[number]]


def segmentPrimes(low, high):
    primes = primeSieve(math.isqrt(high) + 1)
    segment = bytearray(b"\x01") * (high - low + 1)

    for prime in primes:
        start = max(prime * prime, ((low + prime - 1) // prime) * prime)

        for multiple in range(start, high + 1, prime):
            segment[multiple - low] = 0

    return [low + index for index, isPrime in enumerate(segment) if isPrime and low + index > 1]


def primeFactors(number):
    factors = []
    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)

            while number % divisor == 0:
                number //= divisor

        divisor += 1 if divisor == 2 else 2

    if number > 1:
        factors.append(number)

    return factors


def repetendSuffix(prime):
    modulus = prime * SUFFIX_MODULUS
    return ((pow(10, prime - 1, modulus) - 1) // prime) % SUFFIX_MODULUS


def isFullReptendPrime(prime):
    return all(pow(10, (prime - 1) // factor, prime) != 1 for factor in primeFactors(prime - 1))


def cyclicNumberDigitSum():
    low = 10**11 // (PREFIX + 1) + 1
    high = 10**11 // PREFIX

    for prime in segmentPrimes(low, high):
        if repetendSuffix(prime) == SUFFIX and isFullReptendPrime(prime):
            return 9 * (prime - 1) // 2

    raise RuntimeError("No cyclic number found")


def runTests():
    assert 9 * (7 - 1) // 2 == 27


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cyclicNumberDigitSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
