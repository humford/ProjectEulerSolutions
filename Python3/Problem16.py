def powerDigitSum(base, exponent):
    return sum(int(digit) for digit in str(base ** exponent))


def runTests():
    assert powerDigitSum(2, 15) == 26


def solve():
    return powerDigitSum(2, 1000)


if __name__ == "__main__":
    runTests()
    print(solve())
