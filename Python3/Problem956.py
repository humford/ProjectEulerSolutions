from math import isqrt
import time


TARGET_N = 1_000
TARGET_M = 1_000
MODULUS = 999_999_001


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for prime in range(2, isqrt(limit) + 1):
        if isPrime[prime]:
            start = prime * prime
            isPrime[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )

    return [value for value in range(2, limit + 1) if isPrime[value]]


def factorization(value):
    factors = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor += 1 if divisor == 2 else 2

    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def primitiveRoot(prime):
    factors = factorization(prime - 1)
    candidate = 2
    while True:
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
        candidate += 1


def superduperPrimeExponents(limit):
    exponents = {}
    for prime in primeSieve(limit):
        factorialExponent = 0
        total = 0
        for value in range(1, limit + 1):
            reduced = value
            while reduced % prime == 0:
                factorialExponent += 1
                reduced //= prime
            total += (limit - value + 1) * factorialExponent
        exponents[prime] = total
    return exponents


def geometricResidueFactor(prime, exponent, classes):
    coefficients = [0] * classes
    power = 1
    for degree in range(exponent + 1):
        coefficients[degree % classes] += power
        power *= prime
    return coefficients


def exactD(limit, classes):
    coefficients = [1] + [0] * (classes - 1)
    for prime, exponent in superduperPrimeExponents(limit).items():
        factor = geometricResidueFactor(prime, exponent, classes)
        product = [0] * classes
        for leftDegree, leftValue in enumerate(coefficients):
            if leftValue == 0:
                continue
            for rightDegree, rightValue in enumerate(factor):
                product[(leftDegree + rightDegree) % classes] += leftValue * rightValue
        coefficients = product
    return coefficients[0]


def modularD(limit, classes, modulus):
    root = primitiveRoot(modulus)
    omega = pow(root, (modulus - 1) // classes, modulus)
    inverseClasses = pow(classes, -1, modulus)
    exponents = superduperPrimeExponents(limit)

    total = 0
    point = 1
    for _ in range(classes):
        value = 1
        for prime, exponent in exponents.items():
            ratio = (prime * point) % modulus
            if ratio == 1:
                factor = (exponent + 1) % modulus
            else:
                factor = (
                    (pow(ratio, exponent + 1, modulus) - 1)
                    * pow(ratio - 1, -1, modulus)
                ) % modulus
            value = (value * factor) % modulus

        total = (total + value) % modulus
        point = (point * omega) % modulus

    return total * inverseClasses % modulus


def solve():
    return modularD(TARGET_N, TARGET_M, MODULUS)


def runTests():
    assert exactD(6, 6) == 6_368_195_719_791_280
    assert modularD(6, 6, MODULUS) == exactD(6, 6) % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
