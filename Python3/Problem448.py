import math
import time
from array import array


MODULUS = 999_999_017
PROBLEM_LIMIT = 99_999_999_019
SIEVE_LIMIT = 5_000_000


def averageLcm(n):
    return sum(n * value // math.gcd(n, value) for value in range(1, n + 1)) // n


def bruteS(limit):
    return sum(averageLcm(number) for number in range(1, limit + 1))


def sumIntegers(first, last):
    return ((first + last) * (last - first + 1) // 2) % MODULUS


def sumSquares(limit):
    inverseSix = pow(6, -1, MODULUS)
    return (
        (limit % MODULUS)
        * ((limit + 1) % MODULUS)
        % MODULUS
        * ((2 * limit + 1) % MODULUS)
        * inverseSix
    ) % MODULUS


class TotientProductSummatory:
    def __init__(self, sieveLimit=SIEVE_LIMIT):
        self.sieveLimit = sieveLimit
        self.prefix = self.buildPrefix(sieveLimit)
        self.cache = {}

    def buildPrefix(self, limit):
        phi = array("Q", [0]) * (limit + 1)
        phi[1] = 1

        isComposite = bytearray(limit + 1)
        primes = []

        for number in range(2, limit + 1):
            if not isComposite[number]:
                primes.append(number)
                phi[number] = number - 1

            for prime in primes:
                composite = number * prime
                if composite > limit:
                    break

                isComposite[composite] = 1
                if number % prime == 0:
                    phi[composite] = phi[number] * prime
                    break

                phi[composite] = phi[number] * (prime - 1)

        prefix = array("I", [0]) * (limit + 1)
        total = 0

        for number in range(1, limit + 1):
            total = (total + (number % MODULUS) * (phi[number] % MODULUS)) % MODULUS
            prefix[number] = total

        return prefix

    def G(self, limit):
        if limit <= self.sieveLimit:
            return self.prefix[limit]

        if limit in self.cache:
            return self.cache[limit]

        # If g(n)=n*phi(n), then g * id = n^2.  Summing this convolution
        # gives a quotient-grouped recurrence for G(x)=sum_{n<=x} g(n).
        total = sumSquares(limit)
        start = 2

        while start <= limit:
            quotient = limit // start
            end = limit // quotient
            total = (total - sumIntegers(start, end) * self.G(quotient)) % MODULUS
            start = end + 1

        self.cache[limit] = total
        return total


def lcmAverageSum(limit):
    summatory = TotientProductSummatory()
    weightedTotal = 0
    start = 1

    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        weightedTotal = (
            weightedTotal
            + (quotient % MODULUS) * (summatory.G(end) - summatory.G(start - 1))
        ) % MODULUS
        start = end + 1

    return (weightedTotal + limit) * pow(2, -1, MODULUS) % MODULUS


def runTests():
    assert averageLcm(2) == 2
    assert averageLcm(10) == 32
    assert bruteS(100) == 122726
    assert lcmAverageSum(100) == 122726


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lcmAverageSum(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
