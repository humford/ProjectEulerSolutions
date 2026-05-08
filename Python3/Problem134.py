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


def primePairConnection(first, second):
    scale = 10 ** len(str(first))
    multiplier = (-first * pow(scale, -1, second)) % second
    return multiplier * scale + first


def connectionSum(limit):
    primes = primesUpTo(limit + 1000)
    total = 0

    for index, first in enumerate(primes):
        if first < 5:
            continue
        if first > limit:
            break
        total += primePairConnection(first, primes[index + 1])

    return total


def runTests():
    assert primePairConnection(19, 23) == 1219


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = connectionSum(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
