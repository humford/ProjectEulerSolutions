import time
from fractions import Fraction


def generatingFunction(n):
    return sum((-n) ** power for power in range(11))


def interpolateValue(points, x):
    total = Fraction(0)

    for index, (x_i, y_i) in enumerate(points):
        term = Fraction(y_i)
        for other_index, (x_j, _) in enumerate(points):
            if index == other_index:
                continue
            term *= Fraction(x - x_j, x_i - x_j)
        total += term

    return total


def firstIncorrectTerm(function, degree):
    points = [(n, function(n)) for n in range(1, degree + 1)]
    x = degree + 1
    return interpolateValue(points, x)


def sumFITs(function, max_degree):
    return sum(firstIncorrectTerm(function, degree) for degree in range(1, max_degree + 1))


def runTests():
    assert sumFITs(lambda n: n ** 3, 3) == 74


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumFITs(generatingFunction, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
