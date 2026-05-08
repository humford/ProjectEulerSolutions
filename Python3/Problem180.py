import math
import time
from fractions import Fraction


def rationalNumbers(order):
    return {
        Fraction(numerator, denominator)
        for denominator in range(2, order + 1)
        for numerator in range(1, denominator)
    }


def rationalSquareRoot(number):
    numerator_root = math.isqrt(number.numerator)
    denominator_root = math.isqrt(number.denominator)

    if (
        numerator_root * numerator_root == number.numerator
        and denominator_root * denominator_root == number.denominator
    ):
        return Fraction(numerator_root, denominator_root)

    return None


def goldenTripletSum(order):
    rationals = rationalNumbers(order)
    sums = set()

    for x in rationals:
        for y in rationals:
            z = x + y
            if z in rationals:
                sums.add(x + y + z)

            z = x * y / (x + y)
            if z in rationals:
                sums.add(x + y + z)

            square_sum_root = rationalSquareRoot(x * x + y * y)
            if square_sum_root is None:
                continue

            z = square_sum_root
            if z in rationals:
                sums.add(x + y + z)

            z = x * y / square_sum_root
            if z in rationals:
                sums.add(x + y + z)

    total = sum(sums, Fraction(0, 1))
    return total.numerator + total.denominator


def runTests():
    assert goldenTripletSum(10) == 12519


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = goldenTripletSum(35)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
