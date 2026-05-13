from math import exp, lgamma, log
import time


TARGET_A = 89
TARGET_B = 97


def returnProbabilityTerm(a, b, index):
    length = (a + b) * index
    leftSteps = a * index
    rightSteps = b * index
    logTerm = (
        lgamma(length + 1)
        - lgamma(leftSteps + 1)
        - lgamma(rightSteps + 1)
        - length * log(2)
    )
    return exp(logTerm)


def f(a, b, tolerance=1e-18):
    if a == b:
        return 0.0
    if a > b:
        a, b = b, a

    greenFunction = 1.0
    term = 1.0
    index = 1
    while True:
        term = returnProbabilityTerm(a, b, index)
        greenFunction += term
        if term < tolerance:
            break
        index += 1

    return 1.0 / greenFunction


def solve():
    return f(TARGET_A, TARGET_B)


def runTests():
    assert f(1, 1) == 0.0
    assert abs(f(1, 2) - 0.427050983) < 5e-10


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + format(answer, ".9f") + " in " + str(elapsed) + " seconds.")
