from functools import cache
from fractions import Fraction
from math import gcd
import time


LIMIT = 10 ** 18


def primes():
    yield 2
    known_primes = [2]
    candidate = 3

    while True:
        is_prime = True
        for prime in known_primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break

        if is_prime:
            known_primes.append(candidate)
            yield candidate

        candidate += 2


def oddNumeratorSearchLimit(limit):
    product = 1
    quotient_bound = Fraction(1, 1)

    for prime in primes():
        if product * prime > limit:
            break

        product *= prime
        quotient_bound *= Fraction(prime, prime - 1)

    doubled_bound = 2 * quotient_bound
    return doubled_bound.numerator // doubled_bound.denominator + 2


@cache
def smallestPrimeFactor(number):
    if number % 2 == 0:
        return 2

    factor = 3
    while factor * factor <= number:
        if number % factor == 0:
            return factor
        factor += 2

    return number


def halfIntegerPerfectionNumbers(limit):
    result = set()

    def search(number, remaining_numerator, remaining_denominator):
        if number * remaining_denominator > limit:
            return

        if remaining_numerator == 1 and remaining_denominator == 1:
            result.add(number)
            return

        if remaining_denominator == 1:
            return

        prime = smallestPrimeFactor(remaining_denominator)
        if gcd(prime, number) != 1:
            return

        minimum_power = prime
        while remaining_denominator % (minimum_power * prime) == 0:
            minimum_power *= prime

        power = minimum_power
        while number * power <= limit:
            sigma_power = (power * prime - 1) // (prime - 1)
            next_numerator = remaining_numerator * power
            next_denominator = remaining_denominator * sigma_power
            common = gcd(next_numerator, next_denominator)

            search(
                number * power,
                next_numerator // common,
                next_denominator // common,
            )
            power *= prime

    for odd_numerator in range(3, oddNumeratorSearchLimit(limit), 2):
        search(1, odd_numerator, 2)

    return sorted(result)


def sumHalfIntegerPerfectionNumbers(limit):
    return sum(halfIntegerPerfectionNumbers(limit))


def runTests():
    assert oddNumeratorSearchLimit(LIMIT) == 16
    assert halfIntegerPerfectionNumbers(10 ** 4) == [2, 24, 4320, 4680]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumHalfIntegerPerfectionNumbers(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
