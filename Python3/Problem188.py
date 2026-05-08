import math
import time


def phi(number):
    result = number
    factor = 2
    remaining = number

    while factor * factor <= remaining:
        if remaining % factor == 0:
            result -= result // factor
            while remaining % factor == 0:
                remaining //= factor
        factor += 1 if factor == 2 else 2

    if remaining > 1:
        result -= result // remaining

    return result


def hyperexponentiationMod(base, height, modulus):
    if modulus == 1:
        return 0
    if height == 1:
        return base % modulus

    exponent = hyperexponentiationMod(base, height - 1, phi(modulus))
    return pow(base, exponent, modulus)


def runTests():
    assert hyperexponentiationMod(3, 2, 100) == 27
    assert hyperexponentiationMod(3, 3, 100) == 87


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hyperexponentiationMod(1777, 1855, 100000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
