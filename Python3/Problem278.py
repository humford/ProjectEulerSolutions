import math
import time


LIMIT = 5000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    sieve[0] = 0
    sieve[1] = 0

    for number in range(2, math.isqrt(limit - 1) + 1):
        if sieve[number]:
            sieve[number * number : limit : number] = b"\x00" * (
                (limit - 1 - number * number) // number + 1
            )

    return [number for number in range(limit) if sieve[number]]


def semiprimeFrobenius(p, q, r):
    return 2 * p * q * r - p * q - p * r - q * r


def semiprimeCombinationSum(limit):
    primes = primeSieve(limit)
    prime_count = len(primes)
    first_power_sum = sum(primes)
    second_power_sum = sum(prime * prime for prime in primes)
    third_power_sum = sum(prime**3 for prime in primes)

    pair_product_sum = (first_power_sum * first_power_sum - second_power_sum) // 2
    triple_product_sum = (
        first_power_sum**3
        - 3 * first_power_sum * second_power_sum
        + 2 * third_power_sum
    ) // 6

    return 2 * triple_product_sum - (prime_count - 2) * pair_product_sum


def runTests():
    assert semiprimeFrobenius(2, 3, 5) == 29
    assert semiprimeFrobenius(2, 7, 11) == 195
    assert semiprimeCombinationSum(6) == 29


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = semiprimeCombinationSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
