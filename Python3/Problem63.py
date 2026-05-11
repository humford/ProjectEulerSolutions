def powerfulDigitCount():
    count = 0
    exponent = 1

    while len(str(9 ** exponent)) >= exponent:
        for base in range(1, 10):
            if len(str(base ** exponent)) == exponent:
                count += 1
        exponent += 1

    return count


def runTests():
    assert len(str(7 ** 5)) == 5


def solve():
    return powerfulDigitCount()


if __name__ == "__main__":
    runTests()
    print(solve())
