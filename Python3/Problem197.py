import math
import time


def nextValue(value):
    return math.floor(2 ** (30.403243784 - value * value)) * 10 ** -9


def stablePairSum():
    previous = -1.0
    current = nextValue(previous)
    last_sum = None

    while True:
        next_current = nextValue(current)
        pair_sum = f"{current + next_current:.9f}"
        if pair_sum == last_sum:
            return pair_sum

        last_sum = pair_sum
        previous, current = current, next_current


def runTests():
    assert nextValue(-1.0) == 0.7100000000000001


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = stablePairSum()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
