import time


MODULUS = 10**9
PROBLEM_LIMIT = 10**6


def f(n):
    if n % 10 == 0:
        return 0

    value = 0

    while True:
        nextValue = pow(n, value, MODULUS)
        if nextValue == value:
            return value

        value = nextValue


def trailingPowerSum(limit):
    return sum(f(n) for n in range(2, limit + 1))


def runTests():
    assert f(4) == 411_728_896
    assert f(10) == 0
    assert f(157) == 743_757
    assert trailingPowerSum(10**3) == 442_530_011_399


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = trailingPowerSum(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
