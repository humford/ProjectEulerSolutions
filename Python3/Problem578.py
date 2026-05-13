import bisect
import math
import sys
import time
from array import array
from functools import lru_cache


sys.setrecursionlimit(1_000_000)


def primeExponents(n):
    exponents = []
    factor = 2

    while factor * factor <= n:
        if n % factor == 0:
            exponent = 0
            while n % factor == 0:
                n //= factor
                exponent += 1
            exponents.append((factor, exponent))
        factor += 1 if factor == 2 else 2

    if n > 1:
        exponents.append((n, 1))

    return exponents


def isDecreasingPrimePower(n):
    exponents = [exponent for _, exponent in primeExponents(n)]
    return all(left >= right for left, right in zip(exponents, exponents[1:]))


class DecreasingPrimePowerCounter:
    def __init__(self, limit):
        self.limit = limit
        self.sieveLimit = math.isqrt(limit)
        self.primes, self.mobiusPrefix, self.primePi = self.mobiusSieve(
            self.sieveLimit
        )

    @staticmethod
    def mobiusSieve(limit):
        mobius = array("i", [0]) * (limit + 1)
        mobius[1] = 1
        primes = []
        isComposite = bytearray(limit + 1)

        for number in range(2, limit + 1):
            if not isComposite[number]:
                primes.append(number)
                mobius[number] = -1

            for prime in primes:
                value = number * prime
                if value > limit:
                    break

                isComposite[value] = 1
                if number % prime == 0:
                    mobius[value] = 0
                    break
                mobius[value] = -mobius[number]

        mobiusPrefix = array("i", [0]) * (limit + 1)
        primePi = array("I", [0]) * (limit + 1)
        mobiusSum = 0
        primeCount = 0
        primeIndex = 0

        for number in range(1, limit + 1):
            mobiusSum += mobius[number]
            mobiusPrefix[number] = mobiusSum

            if primeIndex < len(primes) and primes[primeIndex] == number:
                primeCount += 1
                primeIndex += 1
            primePi[number] = primeCount

        return primes, mobiusPrefix, primePi

    @lru_cache(maxsize=None)
    def squarefreeCount(self, limit):
        if limit <= 0:
            return 0

        root = math.isqrt(limit)
        total = 0
        divisor = 1

        while divisor <= root:
            quotient = limit // (divisor * divisor)
            nextDivisor = math.isqrt(limit // quotient)
            total += (
                self.mobiusPrefix[nextDivisor] - self.mobiusPrefix[divisor - 1]
            ) * quotient
            divisor = nextDivisor + 1

        return total

    @lru_cache(maxsize=None)
    def squarefreeTailCount(self, primeIndex, limit):
        if limit <= 0:
            return 0

        if limit <= self.sieveLimit:
            primeIndex = min(primeIndex, self.primePi[limit])

            if primeIndex == self.primePi[limit]:
                return 1

            if self.primes[primeIndex] * self.primes[primeIndex] > limit:
                return 1 + self.primePi[limit] - primeIndex

        if primeIndex == 0:
            return self.squarefreeCount(limit)

        prime = self.primes[primeIndex - 1]
        return self.squarefreeTailCount(
            primeIndex - 1, limit
        ) - self.squarefreeTailCount(primeIndex, limit // prime)

    def count(self, limit):
        total = self.squarefreeTailCount(0, limit)
        maxExponent = limit.bit_length()

        def visitCore(startIndex, maxAllowedExponent, value):
            nonlocal total
            root = math.isqrt(limit // value)
            endIndex = bisect.bisect_right(self.primes, root)

            for primeIndex in range(startIndex, endIndex):
                prime = self.primes[primeIndex]
                primePower = prime * prime

                for exponent in range(2, maxAllowedExponent + 1):
                    newValue = value * primePower
                    if newValue > limit:
                        break

                    total += self.squarefreeTailCount(
                        primeIndex + 1, limit // newValue
                    )
                    visitCore(primeIndex + 1, exponent, newValue)
                    primePower *= prime

        visitCore(0, maxExponent, 1)
        return total


def decreasingPrimePowerCount(limit):
    return DecreasingPrimePowerCounter(limit).count(limit)


def runTests():
    excluded = [n for n in range(1, 101) if not isDecreasingPrimePower(n)]
    assert excluded == [18, 50, 54, 75, 90, 98]

    counter = DecreasingPrimePowerCounter(10 ** 6)
    assert counter.count(100) == 94
    assert counter.count(10 ** 6) == 922_052


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = decreasingPrimePowerCount(10 ** 13)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
