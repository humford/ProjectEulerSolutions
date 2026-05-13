import itertools
import time


LIMIT = 5000
MODULUS = 10 ** 16


def primeSieve(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = False
    sieve[1] = False

    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            for multiple in range(number * number, limit + 1, number):
                sieve[multiple] = False

    return sieve


def primeSubsetSums(limit):
    primes = [number for number, prime in enumerate(primeSieve(limit - 1)) if prime]
    max_sum = sum(primes)
    counts = [0] * (max_sum + 1)
    counts[0] = 1
    largest = 0

    for prime in primes:
        largest += prime
        for total in range(largest, prime - 1, -1):
            counts[total] = (counts[total] + counts[total - prime]) % MODULUS

    prime_sums = primeSieve(max_sum)
    return sum(count for total, count in enumerate(counts) if prime_sums[total]) % MODULUS


def brutePrimeSubsetSums(limit):
    primes = [number for number, prime in enumerate(primeSieve(limit - 1)) if prime]
    prime_sums = primeSieve(sum(primes))
    result = 0

    for size in range(len(primes) + 1):
        for subset in itertools.combinations(primes, size):
            if prime_sums[sum(subset)]:
                result += 1

    return result


def runTests():
    assert primeSubsetSums(10) == brutePrimeSubsetSums(10)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeSubsetSums(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
