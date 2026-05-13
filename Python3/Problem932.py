from collections import Counter
from math import gcd, isqrt
import random
import time


TARGET_DIGITS = 16


def isPrime(n):
    if n < 2:
        return False

    smallPrimes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in smallPrimes:
        if n % prime == 0:
            return n == prime

    d = n - 1
    exponent = 0
    while d % 2 == 0:
        d //= 2
        exponent += 1

    for base in (2, 3, 5, 7, 11, 13, 17):
        if base >= n:
            continue

        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(exponent - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True


def pollardRho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(2, n - 1)
        y = x
        divisor = 1

        while divisor == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = gcd(abs(x - y), n)

        if divisor != n:
            return divisor


def primeFactors(n):
    factors = []

    def factor(value):
        if value == 1:
            return
        if isPrime(value):
            factors.append(value)
            return

        divisor = pollardRho(value)
        factor(divisor)
        factor(value // divisor)

    factor(n)
    return factors


def primePowerFactors(n):
    counts = Counter(primeFactors(n))
    return [prime**exponent for prime, exponent in counts.items()]


def crtPair(firstResidue, firstModulus, secondResidue, secondModulus):
    adjustment = (secondResidue - firstResidue) * pow(firstModulus, -1, secondModulus)
    return (firstResidue + firstModulus * (adjustment % secondModulus)) % (
        firstModulus * secondModulus
    )


def idempotentResidues(modulus):
    residues = [(0, 1)]

    for primePower in primePowerFactors(modulus):
        nextResidues = []
        for residue, currentModulus in residues:
            nextResidues.append(
                (crtPair(residue, currentModulus, 0, primePower), currentModulus * primePower)
            )
            nextResidues.append(
                (crtPair(residue, currentModulus, 1, primePower), currentModulus * primePower)
            )
        residues = nextResidues

    return sorted(residue for residue, _ in residues)


def numbers2025WithDigitsAtMost(digits):
    maximumNumber = 10**digits - 1
    maximumRoot = isqrt(maximumNumber)
    numbers = set()

    for bDigits in range(1, digits):
        base = 10**bDigits
        modulus = base - 1
        minimumB = 10 ** (bDigits - 1)

        for residue in idempotentResidues(modulus):
            total = residue
            if total < 2:
                total += modulus

            while total <= maximumRoot and total < base:
                b = total * (base - total) // modulus
                a = total - b
                number = total * total

                if minimumB <= b < base and a > 0 and number <= maximumNumber:
                    numbers.add(number)

                total += modulus

    return numbers


def T(digits):
    return sum(numbers2025WithDigitsAtMost(digits))


def solve():
    return T(TARGET_DIGITS)


def runTests():
    numbers = numbers2025WithDigitsAtMost(4)
    assert numbers == {81, 2025, 3025}
    assert T(4) == 5131


if __name__ == "__main__":
    random.seed(932)
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
