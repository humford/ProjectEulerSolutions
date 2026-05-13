import time


TERM_COUNT = 40


def nextSolution(y, x):
    return 3 * y + 8 * x, y + 3 * x


def swappingCounterTerms(count):
    firstBranch = (5, 2)
    secondBranch = (11, 4)
    terms = []

    while len(terms) < count:
        if firstBranch[1] < secondBranch[1]:
            y, x = firstBranch
            firstBranch = nextSolution(y, x)
        else:
            y, x = secondBranch
            secondBranch = nextSolution(y, x)

        terms.append(x - 1)

    return terms


def swappingCounterSum(count=TERM_COUNT):
    return sum(swappingCounterTerms(count))


def runTests():
    assert swappingCounterTerms(5) == [1, 3, 10, 22, 63]
    assert swappingCounterSum(5) == 99


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = swappingCounterSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
