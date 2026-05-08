import itertools
import math
import time


def countNumbers(length, max_repeat):
    total = 0
    factorials = [math.factorial(n) for n in range(length + 1)]

    for counts in itertools.product(range(max_repeat + 1), repeat=10):
        if sum(counts) != length:
            continue

        arrangements = factorials[length]
        for count in counts:
            arrangements //= factorials[count]

        if counts[0] > 0:
            leading_zero = factorials[length - 1] // factorials[counts[0] - 1]
            for count in counts[1:]:
                leading_zero //= factorials[count]
            arrangements -= leading_zero

        total += arrangements

    return total


def runTests():
    assert countNumbers(2, 1) == 81


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = countNumbers(18, 3)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
