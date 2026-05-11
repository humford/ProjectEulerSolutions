def squareRootConvergentCount(limit):
    numerator = 3
    denominator = 2
    count = 0

    for _ in range(1, limit + 1):
        if len(str(numerator)) > len(str(denominator)):
            count += 1
        numerator, denominator = numerator + 2 * denominator, numerator + denominator

    return count


def runTests():
    assert squareRootConvergentCount(8) == 1


def solve():
    return squareRootConvergentCount(1000)


if __name__ == "__main__":
    runTests()
    print(solve())
