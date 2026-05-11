from math import comb


def latticePaths(gridSize):
    return comb(2 * gridSize, gridSize)


def runTests():
    assert latticePaths(2) == 6


def solve():
    return latticePaths(20)


if __name__ == "__main__":
    runTests()
    print(solve())
