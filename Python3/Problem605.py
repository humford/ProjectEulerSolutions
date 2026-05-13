import fractions
import math
import time


MODULUS = 10 ** 8


def winningStartResidue(n, k):
    return n if k == 1 else k - 1


def winProbability(n, k):
    residue = winningStartResidue(n, k)
    powerOfTwo = 2 ** n
    numerator = powerOfTwo * (residue * (powerOfTwo - 1) + n)
    denominator = (2 ** (residue + 1)) * (powerOfTwo - 1) ** 2
    return fractions.Fraction(numerator, denominator)


def probabilityProduct(n, k):
    if n <= 1_000:
        probability = winProbability(n, k)
        return probability.numerator * probability.denominator

    residue = winningStartResidue(n, k)
    gcdCheck = math.gcd(n, (pow(2, n, n) - 1) % n)
    if gcdCheck != 1:
        raise ValueError("large non-coprime reduction not implemented")

    qMinusOne = (pow(2, n, MODULUS) - 1) % MODULUS
    numerator = (
        pow(2, n - residue - 1, MODULUS)
        * (
            residue * qMinusOne
            + n
        )
    ) % MODULUS
    denominator = qMinusOne * qMinusOne % MODULUS
    return numerator * denominator % MODULUS


def runTests():
    assert winProbability(3, 1) == fractions.Fraction(12, 49)
    assert winProbability(6, 2) == fractions.Fraction(368, 1323)
    assert probabilityProduct(3, 1) == 588
    assert probabilityProduct(6, 2) == 486_864


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = probabilityProduct(10 ** 8 + 7, 10 ** 4 + 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
