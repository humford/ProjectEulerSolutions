import math
import time


LIMIT = 13082761331670030


def primeFactors(number):
    factors = []
    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)
            while number % divisor == 0:
                number //= divisor
        divisor += 1

    if number > 1:
        factors.append(number)

    return factors


def cubeRootsOfOneModPrime(prime):
    return [value for value in range(prime) if pow(value, 3, prime) == 1 % prime]


def combineCongruence(value, modulus, residue, prime):
    multiplier = ((residue - value) * pow(modulus, -1, prime)) % prime
    return value + modulus * multiplier


def modularCubeRootSum(modulus):
    solutions = [0]
    current_modulus = 1

    for prime in primeFactors(modulus):
        roots = cubeRootsOfOneModPrime(prime)
        next_solutions = []

        for solution in solutions:
            for root in roots:
                next_solutions.append(
                    combineCongruence(solution, current_modulus, root, prime)
                )

        solutions = next_solutions
        current_modulus *= prime

    return sum(solution for solution in solutions if 1 < solution < modulus)


def runTests():
    assert modularCubeRootSum(91) == 363


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = modularCubeRootSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
