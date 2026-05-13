from math import comb, factorial
import time


TARGET = 100
MODULUS = 1_000_000_007


def treeCount(vertices, modulus=None):
    if vertices == 1:
        return 1
    if modulus is None:
        return vertices ** (vertices - 2)
    return pow(vertices, vertices - 2, modulus)


def factorialMod(value, modulus):
    result = 1
    for factor in range(2, value + 1):
        result = (result * factor) % modulus
    return result


def F(n, modulus=None):
    total = 0

    for smallerSide in range(1, n // 2 + 1):
        largerSide = n - smallerSide

        if modulus is None:
            term = (
                smallerSide
                * comb(n, smallerSide)
                * treeCount(smallerSide)
                * treeCount(largerSide)
                * smallerSide
                * largerSide
            )
            if smallerSide == largerSide:
                term //= 2
            total += term
        else:
            term = smallerSide % modulus
            term = term * comb(n, smallerSide) % modulus
            term = term * treeCount(smallerSide, modulus) % modulus
            term = term * treeCount(largerSide, modulus) % modulus
            term = term * smallerSide * largerSide % modulus
            if smallerSide == largerSide:
                term = term * pow(2, -1, modulus) % modulus
            total = (total + term) % modulus

    if modulus is None:
        return total * factorial(n - 1)
    return total * factorialMod(n - 1, modulus) % modulus


def solve():
    return F(TARGET, MODULUS)


def runTests():
    assert F(3) == 12
    assert F(4) == 360
    assert F(8) == 16_785_941_760


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
