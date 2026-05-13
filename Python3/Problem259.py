import functools
import fractions
import time


DIGITS = "123456789"


def reachableValues(digits):
    @functools.lru_cache(None)
    def values(start, end):
        result = {fractions.Fraction(int(digits[start:end]), 1)}

        for split in range(start + 1, end):
            left_values = values(start, split)
            right_values = values(split, end)

            for left in left_values:
                for right in right_values:
                    result.add(left + right)
                    result.add(left - right)
                    result.add(left * right)
                    if right:
                        result.add(left / right)

        return result

    return values(0, len(digits))


def reachableIntegerSum(digits):
    return sum(
        value.numerator
        for value in reachableValues(digits)
        if value.denominator == 1 and value.numerator > 0
    )


def runTests():
    assert reachableIntegerSum("1234") == 4179


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reachableIntegerSum(DIGITS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
