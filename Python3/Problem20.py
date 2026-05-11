from math import factorial


def factorialDigitSum(n):
    return sum(int(digit) for digit in str(factorial(n)))


def runTests():
    assert factorialDigitSum(10) == 27


def solve():
    return factorialDigitSum(100)


if __name__ == "__main__":
    runTests()
    print(solve())
