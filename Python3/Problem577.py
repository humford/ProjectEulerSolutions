import math
import time


def hexagonCount(n):
    total = 0

    for widthFactor in range(1, n // 3 + 1):
        remaining = n - 3 * widthFactor
        total += widthFactor * math.comb(remaining + 2, 2)

    return total


def hexagonCountSum(n):
    total = 0

    for widthFactor in range(1, n // 3 + 1):
        remaining = n - 3 * widthFactor
        total += widthFactor * math.comb(remaining + 3, 3)

    return total


def runTests():
    assert hexagonCount(3) == 1
    assert hexagonCount(6) == 12
    assert hexagonCount(20) == 966
    assert sum(hexagonCount(n) for n in range(3, 21)) == hexagonCountSum(20)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hexagonCountSum(12_345)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
