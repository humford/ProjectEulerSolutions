import math
import time


def winningNumerator(turns):
    coefficients = [1]

    for red_count in range(1, turns + 1):
        next_coefficients = [0] * (len(coefficients) + 1)
        for blue_count, coefficient in enumerate(coefficients):
            next_coefficients[blue_count] += coefficient * red_count
            next_coefficients[blue_count + 1] += coefficient
        coefficients = next_coefficients

    return sum(coefficients[turns // 2 + 1 :])


def maximumPrizeFund(turns):
    denominator = math.prod(range(2, turns + 2))
    return denominator // winningNumerator(turns)


def runTests():
    assert maximumPrizeFund(4) == 10


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumPrizeFund(15)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
