import math
import time


LIMIT = 10**16
PRIME_BOUND = 100
MIN_FACTORS = 4


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


def countWithDistinctSmallPrimeFactors(limit, prime_bound, min_factors):
    primes = primeSieve(prime_bound)
    inclusive_limit = limit - 1

    def search(index, product, selected):
        result = 0

        if selected >= min_factors:
            coefficient = math.comb(selected - 1, min_factors - 1)
            if (selected - min_factors) & 1:
                coefficient = -coefficient
            result += coefficient * (inclusive_limit // product)

        for next_index in range(index, len(primes)):
            next_product = product * primes[next_index]
            if next_product > inclusive_limit:
                break
            result += search(next_index + 1, next_product, selected + 1)

        return result

    return search(0, 1, 0)


def runTests():
    assert countWithDistinctSmallPrimeFactors(1000, PRIME_BOUND, MIN_FACTORS) == 23


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = countWithDistinctSmallPrimeFactors(LIMIT, PRIME_BOUND, MIN_FACTORS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
