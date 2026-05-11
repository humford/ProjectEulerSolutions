from math import factorial


DIGIT_FACTORIALS = [factorial(digit) for digit in range(10)]


def digitFactorialSum(n):
    return sum(DIGIT_FACTORIALS[int(digit)] for digit in str(n))


def sumDigitFactorials():
    upper = 7 * DIGIT_FACTORIALS[9]
    return sum(value for value in range(3, upper + 1) if digitFactorialSum(value) == value)


def runTests():
    assert digitFactorialSum(145) == 145


def solve():
    return sumDigitFactorials()


if __name__ == "__main__":
    runTests()
    print(solve())
