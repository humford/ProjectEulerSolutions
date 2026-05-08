import time
from fractions import Fraction


def sideCount(first, last):
    directions = {
        Fraction(edge, sides)
        for sides in range(first, last + 1)
        for edge in range(sides)
    }
    return len(directions)


def runTests():
    assert sideCount(3, 4) == 6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sideCount(1864, 1909)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
