import math
import time


FACTORIAL_ARGUMENT = 13
TARGET_INDEX = 150000


def isPrime(number):
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2

    factor = 3
    while factor * factor <= number:
        if number % factor == 0:
            return False
        factor += 2

    return True


def factorial(number):
    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def primeFactorization(number):
    factors = []
    factor = 2

    while factor * factor <= number:
        if number % factor == 0:
            exponent = 0
            while number % factor == 0:
                number //= factor
                exponent += 1
            factors.append((factor, exponent))

        factor += 1 if factor == 2 else 2

    if number > 1:
        factors.append((number, 1))

    return factors


def divisorsFromFactors(factors):
    divisors = [1]

    for prime, exponent in factors:
        previous = divisors
        divisors = []
        power = 1

        for _ in range(exponent + 1):
            for divisor in previous:
                divisors.append(divisor * power)
            power *= prime

    return divisors


def candidatePrimes(target_phi):
    return sorted(
        divisor + 1
        for divisor in divisorsFromFactors(primeFactorization(target_phi))
        if isPrime(divisor + 1)
    )


def numbersWithTotient(target_phi):
    candidates = candidatePrimes(target_phi)
    results = []

    def search(number, phi, first_index):
        for index in range(first_index, len(candidates)):
            prime = candidates[index]
            next_number = number * prime

            if index == first_index and number % prime == 0:
                next_phi = phi * prime
            else:
                next_phi = phi * (prime - 1)

            if next_phi > target_phi:
                break
            if target_phi % next_phi != 0:
                continue
            if next_phi == target_phi:
                results.append(next_number)
            else:
                search(next_number, next_phi, index)

    search(1, 1, 0)
    return sorted(results)


def nthNumberWithFactorialTotient(argument, index):
    values = numbersWithTotient(factorial(argument))
    return values[index - 1]


def runTests():
    values = numbersWithTotient(factorial(FACTORIAL_ARGUMENT))
    assert values[0] == 6227180929
    assert values[TARGET_INDEX - 1] == 23507044290


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nthNumberWithFactorialTotient(FACTORIAL_ARGUMENT, TARGET_INDEX)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
