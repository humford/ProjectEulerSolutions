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


def primePowerTripleCount(limit):
    primes = primesUpTo(int(limit ** 0.5) + 1)
    squares = [prime ** 2 for prime in primes if prime ** 2 < limit]
    cubes = [prime ** 3 for prime in primes if prime ** 3 < limit]
    fourths = [prime ** 4 for prime in primes if prime ** 4 < limit]
    values = set()

    for square in squares:
        for cube in cubes:
            if square + cube >= limit:
                break
            for fourth in fourths:
                total = square + cube + fourth
                if total >= limit:
                    break
                values.add(total)

    return len(values)


def runTests():
    assert primePowerTripleCount(50) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primePowerTripleCount(50000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
