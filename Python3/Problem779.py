import time


LIMIT = 4_000_000


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, int(limit ** 0.5) + 1):
        if isPrime[n]:
            start = n * n
            isPrime[start:limit + 1:n] = b"\x00" * (((limit - start) // n) + 1)

    return [n for n in range(limit + 1) if isPrime[n]]


def seriesSums(limit=LIMIT):
    primes = primeSieve(limit)
    densityWithoutSmallerPrimeFactors = 1.0
    total = 0.0
    f1Mean = 0.0

    for prime in primes:
        total += densityWithoutSmallerPrimeFactors / (prime * (prime - 1) * (prime - 1))
        f1Mean += densityWithoutSmallerPrimeFactors / (prime * prime * (prime - 1))
        densityWithoutSmallerPrimeFactors *= (prime - 1) / prime

    return total, f1Mean


def tailBound(limit):
    return 1 / (2 * limit * limit)


def runTests():
    primes = [2, 3, 5]
    densityWithoutSmallerPrimeFactors = 1.0
    firstThreeTerms = 0.0
    for prime in primes:
        firstThreeTerms += densityWithoutSmallerPrimeFactors / (prime * (prime - 1) * (prime - 1))
        densityWithoutSmallerPrimeFactors *= (prime - 1) / prime

    assert abs(firstThreeTerms - 131 / 240) < 1e-15
    assert tailBound(LIMIT) < 0.5e-12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer, f1Mean = seriesSums()
    assert format(f1Mean, ".12f") == "0.282419756159"
    elapsed = time.time() - start

    print("Found " + format(answer, ".12f") + " in " + str(elapsed) + " seconds.")
