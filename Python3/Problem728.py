import time
from array import array
from math import gcd


MODULUS = 1_000_000_007


def powersOfTwo(limit):
    powers = array("I", [0]) * (limit + 1)
    value = 1
    powers[0] = value
    for index in range(1, limit + 1):
        value <<= 1
        if value >= MODULUS:
            value -= MODULUS
        powers[index] = value
    return powers


def totients(limit):
    phi = array("I", [0]) * (limit + 1)
    if limit >= 1:
        phi[1] = 1

    composites = bytearray(limit + 1)
    primes = []
    for value in range(2, limit + 1):
        if not composites[value]:
            primes.append(value)
            phi[value] = value - 1
        for prime in primes:
            product = value * prime
            if product > limit:
                break
            composites[product] = 1
            if value % prime == 0:
                phi[product] = phi[value] * prime
                break
            phi[product] = phi[value] * (prime - 1)

    return phi


def inverseTwoPowerMinusOne(powers):
    limit = len(powers) - 1
    inverses = array("I", [0]) * limit
    if limit <= 1:
        return inverses

    inverses[0] = 1
    prefixProduct = 1
    for exponent in range(1, limit):
        denominator = (powers[exponent] - 1) % MODULUS
        if denominator:
            prefixProduct = prefixProduct * denominator % MODULUS
        inverses[exponent] = prefixProduct

    inverseProduct = pow(prefixProduct, MODULUS - 2, MODULUS)
    suffixProduct = 1
    for exponent in range(limit - 1, 0, -1):
        denominator = (powers[exponent] - 1) % MODULUS
        if denominator:
            inverse = inverseProduct * inverses[exponent - 1] % MODULUS
            inverse = inverse * suffixProduct % MODULUS
            inverses[exponent] = inverse
            suffixProduct = suffixProduct * denominator % MODULUS
        else:
            inverses[exponent] = 0

    inverses[0] = 0
    return inverses


def solvableCoinStates(coins, turnCount):
    common = gcd(coins, turnCount)
    if (turnCount & -turnCount) <= (coins & -coins):
        gcdDegree = common - 1
    else:
        gcdDegree = common
    return 1 << (coins - gcdDegree)


def solvableCoinStateSum(limit):
    powers = powersOfTwo(limit)
    phi = totients(limit)
    inverses = inverseTwoPowerMinusOne(powers)
    half = (MODULUS + 1) // 2

    total = 0
    for m in range(1, limit + 1):
        quotientLimit = limit // m
        exponentStep = m - 1

        coefficient = phi[m]
        if m == 1 or m % 2 == 0:
            coefficient = 2 * coefficient % MODULUS
        else:
            coefficient = 3 * coefficient % MODULUS
            coefficient = coefficient * half % MODULUS

        if exponentStep == 0:
            geometric = quotientLimit % MODULUS
        else:
            ratio = powers[exponentStep]
            denominatorInverse = inverses[exponentStep]
            if denominatorInverse == 0:
                geometric = quotientLimit % MODULUS
            else:
                ratioPower = powers[exponentStep * quotientLimit]
                numerator = ratio * (ratioPower - 1) % MODULUS
                geometric = numerator * denominatorInverse % MODULUS

        total = (total + coefficient * geometric) % MODULUS

    return total


def runTests():
    assert solvableCoinStates(3, 2) == 4
    assert solvableCoinStates(8, 3) == 256
    assert solvableCoinStates(9, 3) == 128
    assert solvableCoinStateSum(3) == 22
    assert solvableCoinStateSum(10) == 10_444
    assert solvableCoinStateSum(10**3) == 853_837_042


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solvableCoinStateSum(10**7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
