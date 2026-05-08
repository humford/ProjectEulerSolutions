import time


def countSums(n):
    ways = [0] * (n + 1)
    ways[0] = 1

    for addend in range(1, n):
        for total in range(addend, n + 1):
            ways[total] += ways[total - addend]

    return ways[n]


def runTests():
    assert countSums(5) == 6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = countSums(100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
