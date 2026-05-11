def diagonalSum(dimension):
    total = 1
    value = 1

    for step in range(2, dimension, 2):
        for _ in range(4):
            value += step
            total += value

    return total


def runTests():
    assert diagonalSum(5) == 101


def solve():
    return diagonalSum(1001)


if __name__ == "__main__":
    runTests()
    print(solve())
