from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb, factorial
import time


def primeCount(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = False
    sieve[1] = False

    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            for multiple in range(number * number, limit + 1, number):
                sieve[multiple] = False

    return sum(sieve)


def partialDerangementProbability(disks, marked_disks, moved_marked_disks):
    fixed_marked_disks = marked_disks - moved_marked_disks
    free_disks = disks - fixed_marked_disks

    favorable = comb(marked_disks, fixed_marked_disks) * sum(
        (-1) ** fixed_forbidden
        * comb(moved_marked_disks, fixed_forbidden)
        * factorial(free_disks - fixed_forbidden)
        for fixed_forbidden in range(moved_marked_disks + 1)
    )

    return Fraction(favorable, factorial(disks))


def roundedProbability(disks, marked_disks, moved_marked_disks):
    probability = partialDerangementProbability(disks, marked_disks, moved_marked_disks)
    getcontext().prec = 80
    rounded = (Decimal(probability.numerator) / Decimal(probability.denominator)).quantize(
        Decimal("0.000000000001")
    )

    return format(rounded, "f")


def twentyTwoFoolishPrimes():
    return roundedProbability(100, primeCount(100), 22)


def runTests():
    assert primeCount(100) == 25
    assert roundedProbability(2, 1, 1) == "0.500000000000"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = twentyTwoFoolishPrimes()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
