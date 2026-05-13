import math
import time


def squareInteriorCount(limit):
    gcds = [[0] * (limit + 1) for _ in range(limit + 1)]
    for a in range(1, limit + 1):
        for b in range(1, limit + 1):
            gcds[a][b] = math.gcd(a, b)

    maxInterior = 2 * limit * limit + 1
    squareTargets = [2 * (root * root - 1) for root in range(1, math.isqrt(maxInterior) + 2)]

    total = 0
    for b in range(1, limit + 1):
        gcdB = gcds[b]

        for d in range(1, limit + 1):
            gcdD = gcds[d]
            sideSum = b + d
            values = [sideSum * a - gcdB[a] - gcdD[a] for a in range(1, limit + 1)]

            frequencies = {}
            for value in values:
                frequencies[value] = frequencies.get(value, 0) + 1

            for value in values:
                for target in squareTargets:
                    total += frequencies.get(target - value, 0)

    return total


def runTests():
    assert squareInteriorCount(4) == 42


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squareInteriorCount(100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
