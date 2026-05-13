import itertools
import math
import time
from fractions import Fraction


def firstSortSteps(items):
    items = list(items)
    steps = 0
    while True:
        for index in range(len(items) - 1):
            if items[index] > items[index + 1]:
                value = items.pop(index + 1)
                items.insert(0, value)
                steps += 1
                break
        else:
            return steps


def expectedFirstSortSteps(n):
    # Averaging the process over all permutations gives one independent
    # contribution for each suffix length k.
    return sum(Fraction(2 ** (k - 1) - 1, k) for k in range(1, n + 1))


def formatDecimal(value, digits):
    scale = 10 ** digits
    numerator = value.numerator * scale
    quotient, remainder = divmod(numerator, value.denominator)
    if 2 * remainder >= value.denominator:
        quotient += 1

    whole, decimal = divmod(quotient, scale)
    return str(whole) + "." + str(decimal).zfill(digits)


def runTests():
    assert firstSortSteps([4, 1, 3, 2]) == 5
    total = sum(firstSortSteps(permutation) for permutation in itertools.permutations(range(1, 5)))
    assert Fraction(total, math.factorial(4)) == Fraction(13, 4)
    assert expectedFirstSortSteps(4) == Fraction(13, 4)
    assert formatDecimal(expectedFirstSortSteps(10), 3) == "115.725"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formatDecimal(expectedFirstSortSteps(30), 2)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
