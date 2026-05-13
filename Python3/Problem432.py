from array import array
from functools import lru_cache
import time


BASE_PRIMES = (2, 3, 5, 7, 11, 13, 17)
MODULUS = 1_000_000_000
PRECOMPUTE_LIMIT = 2_000_000


def totients(limit):
    values = array("Q", range(limit + 1))

    for number in range(2, limit + 1):
        if values[number] == number:
            for multiple in range(number, limit + 1, number):
                values[multiple] -= values[multiple] // number

    return values


def baseTotient(modulus=None):
    value = 1

    for prime in BASE_PRIMES:
        value *= prime - 1
        if modulus is not None:
            value %= modulus

    return value


def directS(limit):
    phi = totients(limit)
    multiplier = baseTotient()
    total = 0

    for number in range(1, limit + 1):
        value = phi[number]

        for prime in BASE_PRIMES:
            if number % prime == 0:
                value = value * prime // (prime - 1)

        total += multiplier * value

    return total


class TotientPrefix:
    def __init__(self, limit, modulus=MODULUS):
        self.limit = limit
        self.modulus = modulus
        self.precomputeLimit = min(PRECOMPUTE_LIMIT, limit)
        self.prefix = self.precomputePrefix()

    def precomputePrefix(self):
        phi = totients(self.precomputeLimit)
        prefix = array("I", [0]) * (self.precomputeLimit + 1)
        total = 0

        for number in range(1, self.precomputeLimit + 1):
            total = (total + phi[number]) % self.modulus
            prefix[number] = total

        return prefix

    @lru_cache(maxsize=None)
    def total(self, limit):
        if limit <= self.precomputeLimit:
            return self.prefix[limit]

        total = limit * (limit + 1) // 2 % self.modulus
        lower = 2

        while lower <= limit:
            quotient = limit // lower
            upper = limit // quotient
            total -= (upper - lower + 1) * self.total(quotient)
            total %= self.modulus
            lower = upper + 1

        return total


class CoprimeTotientPrefix:
    def __init__(self, limit, modulus=MODULUS):
        self.modulus = modulus
        self.totientPrefix = TotientPrefix(limit, modulus)

    @lru_cache(maxsize=None)
    def excludingFirstPrimes(self, primeCount, limit):
        if limit <= 0:
            return 0
        if primeCount == 0:
            return self.totientPrefix.total(limit)

        prime = BASE_PRIMES[primeCount - 1]
        total = self.excludingFirstPrimes(primeCount - 1, limit)
        primePower = prime
        phiPrimePower = prime - 1

        while primePower <= limit:
            total -= phiPrimePower * self.excludingFirstPrimes(
                primeCount, limit // primePower
            )
            total %= self.modulus
            primePower *= prime
            phiPrimePower = phiPrimePower * prime % self.modulus

        return total

    def total(self, limit):
        return self.excludingFirstPrimes(len(BASE_PRIMES), limit)


def smoothNumbers(limit):
    values = []

    def search(index, current):
        if index == len(BASE_PRIMES):
            values.append(current)
            return

        prime = BASE_PRIMES[index]
        value = current
        while value <= limit:
            search(index + 1, value)
            value *= prime

    search(0, 1)
    return values


def lastDigits(limit=10**11, modulus=MODULUS):
    coprimePrefix = CoprimeTotientPrefix(limit, modulus)
    total = 0

    for smooth in smoothNumbers(limit):
        total += (smooth % modulus) * coprimePrefix.total(limit // smooth)
        total %= modulus

    return baseTotient(modulus) * total % modulus


def runTests():
    sample = directS(10**6)
    assert sample == 45480596821125120
    assert lastDigits(10**6) == sample % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lastDigits()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
