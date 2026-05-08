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


def primePartitionCount(n):
    ways = [0] * (n + 1)
    ways[0] = 1

    for prime in primesUpTo(n):
        for total in range(prime, n + 1):
            ways[total] += ways[total - prime]

    return ways[n]


def firstWithPrimePartitionsAbove(threshold):
    n = 2
    while True:
        if primePartitionCount(n) > threshold:
            return n
        n += 1


def runTests():
    assert primePartitionCount(10) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstWithPrimePartitionsAbove(5000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
