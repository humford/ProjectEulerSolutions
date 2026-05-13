import time


EXPONENT = 30


def fibonacci(index):
    previous = 0
    current = 1

    for _ in range(index):
        previous, current = current, previous + current

    return previous


def losingNimPositionCount(exponent):
    return fibonacci(exponent + 2)


def bruteLosingNimPositionCount(exponent):
    return sum(
        1
        for n in range(1, 2**exponent + 1)
        if n ^ (2 * n) ^ (3 * n) == 0
    )


def runTests():
    assert losingNimPositionCount(10) == bruteLosingNimPositionCount(10)
    assert losingNimPositionCount(20) == 17711


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = losingNimPositionCount(EXPONENT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
