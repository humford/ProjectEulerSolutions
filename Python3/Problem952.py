from array import array
from math import factorial, isqrt
import time


BASE = 1_000_000_007
TARGET = 10_000_000


def smallestPrimeFactors(limit):
    factors = array("I", range(limit + 1))
    if limit >= 1:
        factors[1] = 1

    for value in range(2, isqrt(limit) + 1):
        if factors[value] == value:
            for multiple in range(value * value, limit + 1, value):
                if factors[multiple] == multiple:
                    factors[multiple] = value

    return factors


def primesFromFactors(factors):
    return [value for value in range(2, len(factors)) if factors[value] == value]


def factorization(value, factors):
    result = {}
    while value > 1:
        prime = factors[value]
        exponent = 0
        while value % prime == 0:
            value //= prime
            exponent += 1
        result[prime] = exponent
    return result


def factorialPrimeExponent(limit, prime):
    total = 0
    while limit:
        limit //= prime
        total += limit
    return total


def twoAdicValuation(value):
    return (value & -value).bit_length() - 1


def updateMaximum(exponents, prime, exponent):
    if exponent > exponents.get(prime, 0):
        exponents[prime] = exponent


def orderModuloPrime(base, prime, factors):
    order = prime - 1
    for factor in factorization(prime - 1, factors):
        while order % factor == 0 and pow(base, order // factor, prime) == 1:
            order //= factor
    return order


def liftingValuation(base, order, prime, maxExponent):
    valuation = 1
    modulus = prime * prime

    while valuation < maxExponent and pow(base, order, modulus) == 1:
        valuation += 1
        modulus *= prime

    return valuation


def R(prime, limit):
    factors = smallestPrimeFactors(limit)
    primes = primesFromFactors(factors)
    orderExponents = {}

    for modulusPrime in primes:
        factorialExponent = factorialPrimeExponent(limit, modulusPrime)

        if modulusPrime == 2:
            if factorialExponent == 1:
                twoPower = 0
            elif prime % 4 == 1:
                twoPower = max(0, factorialExponent - twoAdicValuation(prime - 1))
            else:
                twoPower = max(1, factorialExponent - twoAdicValuation(prime + 1))
            updateMaximum(orderExponents, 2, twoPower)
            continue

        order = orderModuloPrime(prime, modulusPrime, factors)
        for factor, exponent in factorization(order, factors).items():
            updateMaximum(orderExponents, factor, exponent)

        if factorialExponent > 1:
            lifted = liftingValuation(prime, order, modulusPrime, factorialExponent)
            updateMaximum(orderExponents, modulusPrime, factorialExponent - lifted)

    answer = 1
    for orderPrime, exponent in orderExponents.items():
        answer = (answer * pow(orderPrime, exponent, prime)) % prime

    return answer


def bruteR(prime, limit):
    modulus = factorial(limit)
    if modulus == 1:
        return 1

    value = prime % modulus
    current = value
    order = 1
    while current != 1:
        current = (current * value) % modulus
        order += 1
    return order


def solve():
    return R(BASE, TARGET)


def runTests():
    assert R(7, 4) == 2
    assert R(BASE, 12) == 17_280
    for prime in (5, 7, 11, 13):
        for limit in range(1, min(prime, 7)):
            assert R(prime, limit) == bruteR(prime, limit) % prime


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
