import time
from array import array


MODULUS = 1_000_000_087
TARGET = 10_000_000


def smallestPrimeFactors(limit):
    factors = array("I", [0]) * (limit + 1)
    for number in range(2, limit + 1):
        if factors[number] == 0:
            factors[number] = number
            square = number * number
            if square <= limit:
                for multiple in range(square, limit + 1, number):
                    if factors[multiple] == 0:
                        factors[multiple] = number
    return factors


def modularInverses(limit, modulus):
    inverses = array("I", [0]) * (limit + 1)
    inverses[1] = 1
    for value in range(2, limit + 1):
        inverses[value] = (
            modulus - (modulus // value) * inverses[modulus % value] % modulus
        )
    return inverses


def exponentOfTwoInFactorial(limit):
    total = 0
    power = 2
    while power <= limit:
        total += limit // power
        power *= 2
    return total


def factorialOmegaPrefix(limit, modulus=MODULUS):
    factors = smallestPrimeFactors(limit)
    primeExponents = array("I", [0]) * (limit + 1)
    inverses = modularInverses(2 * exponentOfTwoInFactorial(limit) + 1, modulus)

    running = 1
    total = 0
    for number in range(2, limit + 1):
        remaining = number
        while remaining > 1:
            prime = factors[remaining]
            count = 0
            while remaining > 1 and factors[remaining] == prime:
                remaining //= prime
                count += 1

            oldExponent = primeExponents[prime]
            newExponent = oldExponent + count
            running *= 2 * newExponent + 1
            running %= modulus
            running *= inverses[2 * oldExponent + 1]
            running %= modulus
            primeExponents[prime] = newExponent

        total += running
        if total >= modulus:
            total %= modulus

    return total


def runTests():
    assert factorialOmegaPrefix(3) == 12
    assert factorialOmegaPrefix(5) == 96
    assert factorialOmegaPrefix(10) == 4_821


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = factorialOmegaPrefix(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
