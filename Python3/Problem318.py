import math
import time


LIMIT = 2011
REQUIRED_NINES = 2011


def leadingNines(p, q, n):
    rootDifference = math.sqrt(q) - math.sqrt(p)
    if rootDifference >= 1.0:
        return 0

    return int(n * -math.log10(rootDifference * rootDifference))


def minimalPower(p, q, requiredNines=REQUIRED_NINES):
    rootDifference = math.sqrt(q) - math.sqrt(p)
    y = rootDifference * rootDifference
    return math.ceil(requiredNines / -math.log10(y))


def ninesSum(limit=LIMIT, requiredNines=REQUIRED_NINES):
    total = 0

    for p in range(1, limit + 1):
        for q in range(p + 1, limit - p + 1):
            if math.sqrt(q) - math.sqrt(p) < 1.0:
                total += minimalPower(p, q, requiredNines)

    return total


def runTests():
    assert leadingNines(2, 3, 1) == 0
    assert leadingNines(2, 3, 2) == 1
    assert leadingNines(2, 3, 3) == 2


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = ninesSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
