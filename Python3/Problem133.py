import time


def primesUpTo(limit):
    sieve = [True] * limit
    sieve[0] = False
    sieve[1] = False

    for n in range(2, int(limit ** 0.5) + 1):
        if sieve[n]:
            for multiple in range(n * n, limit, n):
                sieve[multiple] = False

    return [n for n in range(limit) if sieve[n]]


def primeFactors(n):
    factors = set()
    factor = 2

    while factor * factor <= n:
        while n % factor == 0:
            factors.add(factor)
            n //= factor
        factor += 1 if factor == 2 else 2

    if n > 1:
        factors.add(n)
    return factors


def repunitPeriodForPrime(prime):
    if prime == 3:
        return 3

    period = prime - 1
    for factor in primeFactors(period):
        while period % factor == 0 and pow(10, period // factor, prime) == 1:
            period //= factor
    return period


def isTwoFiveSmooth(n):
    while n % 2 == 0:
        n //= 2
    while n % 5 == 0:
        n //= 5
    return n == 1


def neverRepunitPowerPrimeSum(limit):
    total = 0

    for prime in primesUpTo(limit):
        if prime in (2, 5):
            total += prime
        elif not isTwoFiveSmooth(repunitPeriodForPrime(prime)):
            total += prime

    return total


def runTests():
    assert repunitPeriodForPrime(7) == 6
    assert repunitPeriodForPrime(41) == 5
    assert not isTwoFiveSmooth(repunitPeriodForPrime(3))
    assert isTwoFiveSmooth(repunitPeriodForPrime(11))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = neverRepunitPowerPrimeSum(100000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
