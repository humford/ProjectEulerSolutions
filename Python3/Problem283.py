import math
import time
from array import array


LIMIT = 1000


def smallestPrimeFactors(limit):
    smallest = array("I", [0]) * (limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if smallest[number] == 0:
            smallest[number] = number
            primes.append(number)

        for prime in primes:
            value = number * prime
            if value > limit or prime > smallest[number]:
                break
            smallest[value] = prime

    return smallest


def factor(number, smallest):
    factors = {}

    while number > 1:
        prime = smallest[number]
        power = 0

        while number % prime == 0:
            number //= prime
            power += 1

        factors[prime] = factors.get(prime, 0) + power

    return factors


def mergeFactors(first, second):
    result = first.copy()

    for prime, power in second.items():
        result[prime] = result.get(prime, 0) + power

    return result


def divisorsFromFactors(factors):
    divisors = [1]

    for prime, power in factors.items():
        previous = divisors[:]
        multiplier = 1

        for _ in range(power):
            multiplier *= prime
            for divisor in previous:
                divisors.append(divisor * multiplier)

    return divisors


def integerAreaRatioPerimeterSum(limit):
    smallest = smallestPrimeFactors(16 * limit * limit)
    total = 0

    for ratio in range(1, limit + 1):
        coefficient = 4 * ratio * ratio
        coefficient_factors = factor(coefficient, smallest)

        for x in range(1, math.isqrt(3 * coefficient) + 1):
            other_factor = coefficient + x * x
            factors = mergeFactors(coefficient_factors, factor(other_factor, smallest))
            product = coefficient * other_factor

            for divisor in divisorsFromFactors(factors):
                if divisor * divisor > product:
                    continue
                if (divisor + coefficient) % x != 0:
                    continue

                paired_divisor = product // divisor
                if (paired_divisor + coefficient) % x != 0:
                    continue

                y = (divisor + coefficient) // x
                z = (paired_divisor + coefficient) // x

                if x <= y <= z:
                    total += 2 * (x + y + z)

    return total


def runTests():
    assert integerAreaRatioPerimeterSum(1) == 192
    assert integerAreaRatioPerimeterSum(10) == 3781786


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = integerAreaRatioPerimeterSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
