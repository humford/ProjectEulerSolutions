from functools import lru_cache
from math import isqrt
import time


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0:1] = b"\x00"
    if limit >= 1:
        sieve[1:2] = b"\x00"

    for number in range(2, isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start:limit + 1:number] = b"\x00" * ((limit - start) // number + 1)

    return [number for number in range(limit + 1) if sieve[number]]


def characterMod3(value):
    if value % 3 == 0:
        return 0
    return 1 if value % 3 == 1 else -1


def integerCharacterPrefix(limit):
    if limit <= 1:
        return 0
    return (1 if limit % 3 == 1 else 0) - 1


class PrimeSummatorySieve:
    def __init__(self, limit):
        self.limit = limit
        self.primes = primeSieve(isqrt(limit))
        values = []
        index = 1

        while index <= limit:
            value = limit // index
            values.append(value)
            index = limit // value + 1

        primeCounts = {value: value - 1 for value in values}
        characterSums = {value: integerCharacterPrefix(value) for value in values}

        for prime in self.primes:
            if primeCounts[prime] == primeCounts[prime - 1]:
                continue

            previousPrimeCount = primeCounts[prime - 1]
            previousCharacterSum = characterSums[prime - 1]
            primeCharacter = characterMod3(prime)
            primeSquare = prime * prime

            for value in values:
                if value < primeSquare:
                    break
                primeCounts[value] -= primeCounts[value // prime] - previousPrimeCount
                characterSums[value] -= (
                    primeCharacter * (characterSums[value // prime] - previousCharacterSum)
                )

        self.primeCounts = primeCounts
        self.characterSums = characterSums

    def primeCount(self, limit):
        return self.primeCounts[limit]

    def primeCharacterSum(self, limit):
        return self.characterSums[limit]


class MultiplicativeSummer:
    def __init__(self, primeSums, mode):
        self.primeSums = primeSums
        self.mode = mode
        self.primes = primeSums.primes
        self.buildSearch()

    def primeValueSum(self, limit):
        primeCount = self.primeSums.primeCount(limit)

        if self.mode == "oddTauSquare":
            return primeCount * 3 - (3 if limit >= 2 else 0)
        if self.mode == "coprimeSixTauSquare":
            return (
                primeCount * 3
                - (3 if limit >= 2 else 0)
                - (3 if limit >= 3 else 0)
            )

        return (
            primeCount
            - (1 if limit >= 3 else 0)
            + 2 * self.primeSums.primeCharacterSum(limit)
        )

    def primePowerValue(self, prime, exponent):
        if self.mode == "oddTauSquare":
            return 0 if prime == 2 else 2 * exponent + 1
        if self.mode == "coprimeSixTauSquare":
            return 0 if prime in (2, 3) else 2 * exponent + 1

        if prime == 3:
            return 0
        if prime % 3 == 1:
            return 2 * exponent + 1
        return -1 if exponent % 2 else 1

    def buildSearch(self):
        primes = self.primes

        @lru_cache(maxsize=None)
        def search(limit, primeIndex):
            previousPrime = primes[primeIndex - 1] if primeIndex else 1
            total = self.primeValueSum(limit) - self.primeValueSum(previousPrime)
            index = primeIndex

            while index < len(primes) and primes[index] * primes[index] <= limit:
                prime = primes[index]
                primePower = prime
                exponent = 1

                while primePower * prime <= limit:
                    value = self.primePowerValue(prime, exponent)
                    if value:
                        total += value * search(limit // primePower, index + 1)
                    total += self.primePowerValue(prime, exponent + 1)
                    primePower *= prime
                    exponent += 1

                index += 1

            return total

        self.search = search

    def sumTo(self, limit):
        return self.search(limit, 0) + 1


class NecklaceCounter:
    def __init__(self, limit):
        self.limit = limit
        primeSums = PrimeSummatorySieve(limit)
        self.sums = {
            "oddTauSquare": MultiplicativeSummer(primeSums, "oddTauSquare").sumTo,
            "coprimeSixTauSquare": MultiplicativeSummer(
                primeSums, "coprimeSixTauSquare"
            ).sumTo,
            "characterWeighted": MultiplicativeSummer(
                primeSums, "characterWeighted"
            ).sumTo,
        }

    def tauTwoSquareSum(self, limit):
        total = 0
        power = 1
        exponent = 0

        while power <= limit:
            total += (2 * exponent + 2) * self.sums["oddTauSquare"](limit // power)
            power *= 2
            exponent += 1

        return total

    def tauTwelveSquareSum(self, limit):
        total = 0
        powerTwo = 1
        exponentTwo = 0

        while powerTwo <= limit:
            powerThree = 1
            exponentThree = 0

            while powerTwo * powerThree <= limit:
                total += (
                    (2 * exponentTwo + 3)
                    * (2 * exponentThree + 2)
                    * self.sums["coprimeSixTauSquare"](limit // (powerTwo * powerThree))
                )
                powerThree *= 3
                exponentThree += 1

            powerTwo *= 2
            exponentTwo += 1

        return total

    @lru_cache(maxsize=None)
    def sixthChainCount(self, limit):
        total = 0
        power = 1
        exponent = 0

        while power <= limit:
            total += (
                (2 * exponent + 3)
                * self.sums["coprimeSixTauSquare"](limit // power)
            )
            power *= 2
            exponent += 1

        return total

    def congruenceRestrictedCount(self, limit):
        total = (
            self.sixthChainCount(limit) - self.sums["characterWeighted"](limit)
        ) // 2
        power = 3
        exponent = 1

        while power <= limit:
            total += (2 * exponent - 1) * self.sixthChainCount(limit // power)
            power *= 3
            exponent += 1

        return total

    def count(self):
        return (
            self.tauTwelveSquareSum(self.limit)
            + self.tauTwoSquareSum(self.limit)
            + self.congruenceRestrictedCount(self.limit)
        )


def isNecklaceTriplet(a, b, c):
    numerator = a * c
    denominator = numerator + b * (a + b + c)

    return (
        4 * numerator == denominator
        or 2 * numerator == denominator
        or 4 * numerator == 3 * denominator
    )


def T(limit):
    return NecklaceCounter(limit).count()


def runTests():
    assert isNecklaceTriplet(5, 5, 5)
    assert isNecklaceTriplet(4, 3, 21)
    assert not isNecklaceTriplet(2, 2, 5)
    assert T(1) == 9
    assert T(20) == 732
    assert T(3000) == 438106


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = T(1_000_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
