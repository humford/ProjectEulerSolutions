import time
from array import array


def totientSieve(limit):
    totients = array("I", range(limit + 1))

    for n in range(2, limit + 1):
        if totients[n] == n:
            for multiple in range(n, limit + 1, n):
                totients[multiple] -= totients[multiple] // n

    return totients


def reducedProperFractionCount(limit):
    return sum(totientSieve(limit)[2:])


def runTests():
    assert reducedProperFractionCount(8) == 21


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reducedProperFractionCount(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
