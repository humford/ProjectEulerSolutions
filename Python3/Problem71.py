import math
import time


def numeratorLeftOfThreeSevenths(limit):
    best_n = 0
    best_d = 1

    for d in range(2, limit + 1):
        n = (3 * d - 1) // 7
        if math.gcd(n, d) == 1 and n * best_d > best_n * d:
            best_n = n
            best_d = d

    return best_n


def runTests():
    assert numeratorLeftOfThreeSevenths(8) == 2


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = numeratorLeftOfThreeSevenths(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
