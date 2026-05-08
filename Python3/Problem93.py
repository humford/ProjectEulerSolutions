import itertools
import time
from fractions import Fraction


def expressionValues(numbers):
    numbers = tuple(Fraction(number) for number in numbers)

    def search(values):
        if len(values) == 1:
            return {values[0]}

        results = set()
        for first_index in range(len(values)):
            for second_index in range(first_index + 1, len(values)):
                first = values[first_index]
                second = values[second_index]
                rest = [
                    values[index]
                    for index in range(len(values))
                    if index not in (first_index, second_index)
                ]
                candidates = {first + second, first * second, first - second, second - first}
                if second != 0:
                    candidates.add(first / second)
                if first != 0:
                    candidates.add(second / first)

                for candidate in candidates:
                    results.update(search(tuple(rest + [candidate])))

        return results

    return search(numbers)


def consecutiveLength(numbers):
    positive_integers = {
        value.numerator
        for value in expressionValues(numbers)
        if value.denominator == 1 and value.numerator > 0
    }
    n = 1
    while n in positive_integers:
        n += 1
    return n - 1


def bestDigitSet():
    best_length = 0
    best_digits = None

    for digits in itertools.combinations(range(1, 10), 4):
        length = consecutiveLength(digits)
        if length > best_length:
            best_length = length
            best_digits = digits

    return "".join(str(digit) for digit in best_digits)


def runTests():
    assert consecutiveLength((1, 2, 3, 4)) == 28


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = bestDigitSet()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
