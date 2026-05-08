import math
import time


def sqrtContinuedFractionTerms(number):
    root = math.isqrt(number)
    m = 0
    d = 1
    a = root

    yield a

    while True:
        m = d * a - m
        d = (number - m * m) // d
        a = (root + m) // d
        yield a


def isCloserToSqrt(candidate, current, number):
    p1, q1 = candidate
    p2, q2 = current
    side1 = p1 * p1 - number * q1 * q1
    side2 = p2 * p2 - number * q2 * q2

    if side1 < 0 and side2 < 0:
        return p1 * q2 > p2 * q1
    if side1 > 0 and side2 > 0:
        return p1 * q2 < p2 * q1

    sum_numerator = p1 * q2 + p2 * q1
    sum_denominator = q1 * q2
    sum_is_above_twice_root = (
        sum_numerator * sum_numerator
        > 4 * number * sum_denominator * sum_denominator
    )

    if side1 < 0:
        return sum_is_above_twice_root
    return not sum_is_above_twice_root


def bestApproximationDenominator(number, denominator_bound):
    terms = sqrtContinuedFractionTerms(number)
    previous_numerator, numerator = 0, 1
    previous_denominator, denominator = 1, 0
    last = None
    previous = None

    for term in terms:
        next_numerator = term * numerator + previous_numerator
        next_denominator = term * denominator + previous_denominator

        if next_denominator > denominator_bound:
            k = (denominator_bound - previous[1]) // last[1]
            intermediate = (
                previous[0] + k * last[0],
                previous[1] + k * last[1],
            )
            if k > 0 and isCloserToSqrt(intermediate, last, number):
                return intermediate[1]
            return last[1]

        previous = last
        last = (next_numerator, next_denominator)
        previous_numerator, numerator = numerator, next_numerator
        previous_denominator, denominator = denominator, next_denominator


def denominatorSum(limit, denominator_bound):
    total = 0

    for number in range(2, limit + 1):
        if math.isqrt(number) ** 2 != number:
            total += bestApproximationDenominator(number, denominator_bound)

    return total


def runTests():
    assert bestApproximationDenominator(13, 20) == 5
    assert bestApproximationDenominator(13, 30) == 28


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = denominatorSum(100000, 10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
