def distinctTerms(aMax, bMax):
    return len({a ** b for a in range(2, aMax + 1) for b in range(2, bMax + 1)})


def runTests():
    assert distinctTerms(5, 5) == 15


def solve():
    return distinctTerms(100, 100)


if __name__ == "__main__":
    runTests()
    print(solve())
