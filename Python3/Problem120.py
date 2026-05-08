import time


def maximumRemainder(a):
    if a % 2 == 1:
        return a * (a - 1)
    return a * (a - 2)


def sumMaximumRemainders(start, end):
    return sum(maximumRemainder(a) for a in range(start, end + 1))


def runTests():
    assert maximumRemainder(7) == 42


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumMaximumRemainders(3, 1000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
