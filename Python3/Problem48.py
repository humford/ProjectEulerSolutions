def selfPowersLastDigits(limit, digits):
    modulus = 10 ** digits
    total = sum(pow(value, value, modulus) for value in range(1, limit + 1))
    return str(total % modulus).zfill(digits)


def runTests():
    assert selfPowersLastDigits(10, 10) == "0405071317"


def solve():
    return selfPowersLastDigits(1000, 10)


if __name__ == "__main__":
    runTests()
    print(solve())
