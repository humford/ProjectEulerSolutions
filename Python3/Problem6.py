def sumOfSquares(n):
    return n * (n + 1) * (2 * n + 1) // 6


def squareOfSum(n):
    total = n * (n + 1) // 2
    return total ** 2


def sumSquareDifference(n):
    return squareOfSum(n) - sumOfSquares(n)


def runTests():
    assert sumSquareDifference(10) == 2640


def solve():
    return sumSquareDifference(100)


if __name__ == "__main__":
    runTests()
    print(solve())
