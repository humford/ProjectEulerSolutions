def digitPowerSum(n, power):
    return sum(int(digit) ** power for digit in str(n))


def upperSearchLimit(power):
    digits = 1
    while 10 ** (digits - 1) <= digits * (9 ** power):
        digits += 1
    return (digits - 1) * (9 ** power)


def sumDigitNthPowers(power):
    return sum(
        value
        for value in range(2, upperSearchLimit(power) + 1)
        if digitPowerSum(value, power) == value
    )


def runTests():
    assert sumDigitNthPowers(4) == 19316


def solve():
    return sumDigitNthPowers(5)


if __name__ == "__main__":
    runTests()
    print(solve())
