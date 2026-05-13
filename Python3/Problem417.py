import time
from array import array
from functools import lru_cache
from math import lcm


def smallestOddPrimeFactors(limit):
    factors = array("I", [0]) * (limit // 2 + 1)

    for number in range(3, int(limit**0.5) + 1, 2):
        if factors[number // 2] == 0:
            for multiple in range(number * number, limit + 1, 2 * number):
                index = multiple // 2

                if factors[index] == 0:
                    factors[index] = number

    return factors


def factorization(number, smallestOddFactors):
    factors = []

    if number % 2 == 0:
        exponent = 0

        while number % 2 == 0:
            number //= 2
            exponent += 1

        factors.append((2, exponent))

    while number > 1:
        prime = smallestOddFactors[number // 2] or number
        exponent = 0

        while number % prime == 0:
            number //= prime
            exponent += 1

        factors.append((prime, exponent))

    return factors


@lru_cache(maxsize=None)
def smoothMultiplierCount(limit):
    count = 0
    powerOfTwo = 1

    while powerOfTwo <= limit:
        multiplier = powerOfTwo

        while multiplier <= limit:
            count += 1
            multiplier *= 5

        powerOfTwo *= 2

    return count


class CycleLengthCounter:
    def __init__(self, limit):
        self.smallestOddFactors = smallestOddPrimeFactors(limit)

    def multiplicativeOrder(self, modulus):
        if modulus == 1:
            return 0

        totient = modulus

        for prime, _ in factorization(modulus, self.smallestOddFactors):
            totient = totient // prime * (prime - 1)

        order = totient

        for prime, _ in factorization(totient, self.smallestOddFactors):
            while order % prime == 0 and pow(10, order // prime, modulus) == 1:
                order //= prime

        return order

    def cycleLength(self, denominator):
        while denominator % 2 == 0:
            denominator //= 2

        while denominator % 5 == 0:
            denominator //= 5

        return self.multiplicativeOrder(denominator)

    def cycleLengthSum(self, limit):
        total = 0

        for base in range(1, limit + 1, 10):
            for denominator in (base, base + 2, base + 6, base + 8):
                if denominator <= limit:
                    total += self.multiplicativeOrder(
                        denominator
                    ) * smoothMultiplierCount(limit // denominator)

        return total


def runTests(counter):
    assert [counter.cycleLength(number) for number in range(2, 11)] == [
        0,
        1,
        0,
        0,
        1,
        6,
        0,
        1,
        0,
    ]
    assert lcm(counter.cycleLength(3), counter.cycleLength(7)) == counter.cycleLength(
        21
    )
    assert counter.cycleLengthSum(1_000_000) == 55535191115


if __name__ == "__main__":
    start = time.time()
    counter = CycleLengthCounter(100_000_000)
    runTests(counter)
    answer = counter.cycleLengthSum(100_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
