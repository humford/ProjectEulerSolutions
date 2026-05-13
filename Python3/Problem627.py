from functools import lru_cache
from math import comb
import time


MODULUS = 1_000_000_007
POLYNOMIAL_DEGREE = 10


def primeList(limit):
    primes = []
    for number in range(2, limit + 1):
        if all(number % prime != 0 for prime in primes if prime * prime <= number):
            primes.append(number)
    return primes


def exponentVectors(maxFactor):
    primes = primeList(maxFactor)
    vectors = []
    for factor in range(1, maxFactor + 1):
        remaining = factor
        vector = []
        for prime in primes:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            vector.append(exponent)
        vectors.append(tuple(vector))
    return vectors


def exactProductCount(maxFactor, factorCount):
    vectors = exponentVectors(maxFactor)
    dimension = len(vectors[0])
    products = {(0,) * dimension}
    for _ in range(factorCount):
        products = {
            tuple(left[index] + right[index] for index in range(dimension))
            for left in products
            for right in vectors
        }
    return len(products)


@lru_cache(maxsize=None)
def smallExponentCount(smallSlots, sevenCount, elevenThirteenCount):
    """Count possible exponents of 2, 3, and 5 after grouping large primes."""
    total = 0
    maxFiveExponent = 2 * smallSlots
    maxTwoThreeFive = 6 * smallSlots + 2 * sevenCount
    boundOne = 4 * smallSlots + 2 * sevenCount + elevenThirteenCount
    boundTwo = 6 * smallSlots + 2 * sevenCount + elevenThirteenCount
    boundThree = 9 * smallSlots + 4 * sevenCount + 2 * elevenThirteenCount

    for fiveExponent in range(maxFiveExponent + 1):
        maxThreeExponent = (maxTwoThreeFive - 3 * fiveExponent) // 2
        for threeExponent in range(maxThreeExponent + 1):
            maxTwoExponent = min(
                boundOne - threeExponent - 2 * fiveExponent,
                boundTwo - 2 * threeExponent - 3 * fiveExponent,
                (boundThree - 3 * threeExponent - 4 * fiveExponent) // 2,
            )
            if maxTwoExponent >= 0:
                total += maxTwoExponent + 1
    return total


def directProductCount30(factorCount):
    total = 0
    for sevenCount in range(factorCount + 1):
        for elevenThirteenCount in range(factorCount - sevenCount + 1):
            remaining = factorCount - sevenCount - elevenThirteenCount
            elevenThirteenChoices = elevenThirteenCount + 1

            for smallSlots in range(remaining + 1):
                plainLargeCount = remaining - smallSlots
                plainLargeChoices = comb(plainLargeCount + 3, 3)
                total += (
                    elevenThirteenChoices
                    * plainLargeChoices
                    * smallExponentCount(
                        smallSlots, sevenCount, elevenThirteenCount
                    )
                )
    return total


def forwardCoefficients(values):
    coefficients = []
    row = values[:]
    while row:
        coefficients.append(row[0])
        row = [row[index + 1] - row[index] for index in range(len(row) - 1)]
    return coefficients


def evaluateForwardPolynomial(coefficients, value):
    return sum(
        coefficient * comb(value, index)
        for index, coefficient in enumerate(coefficients)
    )


def productCount(maxFactor, factorCount):
    if maxFactor != 30:
        return exactProductCount(maxFactor, factorCount)

    initialValues = [
        directProductCount30(index) for index in range(POLYNOMIAL_DEGREE + 1)
    ]
    coefficients = forwardCoefficients(initialValues)
    return evaluateForwardPolynomial(coefficients, factorCount)


def runTests():
    assert exactProductCount(9, 2) == 36
    assert productCount(30, 2) == 308

    directValue = directProductCount30(POLYNOMIAL_DEGREE + 1)
    initialValues = [
        directProductCount30(index) for index in range(POLYNOMIAL_DEGREE + 1)
    ]
    coefficients = forwardCoefficients(initialValues)
    assert coefficients[-1] == 59
    assert evaluateForwardPolynomial(
        coefficients, POLYNOMIAL_DEGREE + 1
    ) == directValue


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = productCount(30, 10_001) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
