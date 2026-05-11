def rightTriangleSolutionCount(perimeter):
    count = 0
    for a in range(1, perimeter // 3):
        numerator = perimeter * (perimeter - 2 * a)
        denominator = 2 * (perimeter - a)
        if numerator % denominator == 0:
            count += 1
    return count


def perimeterWithMostSolutions(limit):
    return max(range(2, limit + 1, 2), key=rightTriangleSolutionCount)


def runTests():
    assert rightTriangleSolutionCount(120) == 3


def solve():
    return perimeterWithMostSolutions(1000)


if __name__ == "__main__":
    runTests()
    print(solve())
