import math
import time


def stringsWithOneAscent(length, alphabet_size):
    return math.comb(alphabet_size, length) * (2 ** length - length - 1)


def maximumStringCount(alphabet_size):
    return max(stringsWithOneAscent(length, alphabet_size) for length in range(1, alphabet_size + 1))


def runTests():
    assert stringsWithOneAscent(3, 26) == 10400


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumStringCount(26)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
