import time


def primesUpTo(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = False
    sieve[1] = False

    for n in range(2, int(limit ** 0.5) + 1):
        if sieve[n]:
            for multiple in range(n * n, limit + 1, n):
                sieve[multiple] = False

    return [n for n in range(limit + 1) if sieve[n]]


def leastPrimeRemainderIndex(threshold):
    limit = 100

    while True:
        primes = primesUpTo(limit)
        for index, prime in enumerate(primes, start=1):
            if index % 2 == 1 and 2 * index * prime > threshold:
                return index
        limit *= 2


def runTests():
    assert leastPrimeRemainderIndex(10 ** 9) == 7037


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastPrimeRemainderIndex(10 ** 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
