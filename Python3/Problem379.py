import math
import time


LIMIT = 10**12


def smallestPrimeFactorSieve(limit):
    smallestPrimeFactor = list(range(limit + 1))

    for number in range(2, math.isqrt(limit) + 1):
        if smallestPrimeFactor[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if smallestPrimeFactor[multiple] == multiple:
                    smallestPrimeFactor[multiple] = number

    return smallestPrimeFactor


def squareFreeDivisorTerms(number, smallestPrimeFactor):
    terms = [(1, 1)]

    while number > 1:
        prime = smallestPrimeFactor[number]
        terms += [(divisor * prime, -sign) for divisor, sign in terms]

        while number % prime == 0:
            number //= prime

    return terms


def floorSumFrom(limit, firstDenominator):
    if firstDenominator > limit:
        return 0

    total = 0
    denominator = firstDenominator

    while denominator <= limit:
        quotient = limit // denominator
        lastDenominator = limit // quotient
        total += quotient * (lastDenominator - denominator + 1)
        denominator = lastDenominator + 1

    return total


def leastCommonMultipleCountSum(limit=LIMIT):
    root = math.isqrt(limit)
    smallestPrimeFactor = smallestPrimeFactorSieve(root)

    # Count reduced pairs (a, b), gcd(a, b) = 1, by scaling them with any d.
    total = limit + floorSumFrom(limit, 2)

    for first in range(2, root + 1):
        reducedLimit = limit // first

        for divisor, sign in squareFreeDivisorTerms(first, smallestPrimeFactor):
            total += sign * floorSumFrom(reducedLimit // divisor, first // divisor + 1)

    return total


def leastCommonMultipleCountSumBrute(limit):
    total = 0

    for first in range(1, limit + 1):
        for second in range(first, limit + 1):
            if math.lcm(first, second) <= limit:
                total += 1

    return total


def runTests():
    assert leastCommonMultipleCountSumBrute(24) == 99
    assert leastCommonMultipleCountSum(24) == 99
    assert leastCommonMultipleCountSum(10**6) == 37429395


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastCommonMultipleCountSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
