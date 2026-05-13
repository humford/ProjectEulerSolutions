import time
from fractions import Fraction


LIMIT = 10_000_000_000
TURNS = 4000


def whiteExpectationExact(disks, turns):
    total = Fraction(0)

    for index in range(1, disks + 1):
        flipProbability = Fraction(2 * index * (disks - index + 1) - 1, disks * disks)
        total += (1 + (1 - 2 * flipProbability) ** turns) / 2

    return total


def whiteExpectation(disks=LIMIT, turns=TURNS):
    if disks <= 10_000:
        return float(whiteExpectationExact(disks, turns))

    halfSum = 0.0
    index = 1

    while True:
        flipProbability = (2 * index * (disks - index + 1) - 1) / (disks * disks)
        term = (1 - 2 * flipProbability) ** turns

        if term < 1e-16:
            break

        halfSum += term
        index += 1

    return disks / 2 + halfSum


def answer():
    return format(whiteExpectation(), ".2f")


def runTests():
    assert whiteExpectationExact(3, 1) == Fraction(10, 9)
    assert whiteExpectationExact(3, 2) == Fraction(5, 3)
    assert format(whiteExpectation(10, 4), ".3f") == "5.157"
    assert format(whiteExpectation(100, 10), ".3f") == "51.893"


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
