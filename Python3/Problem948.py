from math import comb
import time


TARGET = 60


def catalan(index):
    return comb(2 * index, index) // (index + 1)


def F(length):
    sideClassCount = comb(length - 1, (length - 1) // 2)
    exceptional = catalan(length // 2 - 1) if length % 2 == 0 else 0
    return 2**length - 2 * sideClassCount - exceptional


def runTests():
    assert F(3) == 4
    assert F(8) == 181


def solve():
    return F(TARGET)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
