def digitSum(n):
    return sum(int(digit) for digit in str(n))


def powerfulDigitSum(limit):
    return max(digitSum(a ** b) for a in range(1, limit) for b in range(1, limit))


def runTests():
    assert digitSum(12345) == 15


def solve():
    return powerfulDigitSum(100)


if __name__ == "__main__":
    runTests()
    print(solve())
