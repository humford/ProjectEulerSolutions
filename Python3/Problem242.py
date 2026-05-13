import time


LIMIT = 10 ** 12


def weightedPopcountPrefix(limit):
    if limit < 0:
        return 0
    if limit == 0:
        return 1

    highest_bit = limit.bit_length() - 1
    highest_power = 1 << highest_bit

    return 3 ** highest_bit + 2 * weightedPopcountPrefix(limit - highest_power)


def oddTriplets(limit):
    return weightedPopcountPrefix((limit - 1) // 4)


def runTests():
    assert oddTriplets(10) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = oddTriplets(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
