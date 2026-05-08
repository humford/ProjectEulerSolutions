import time


def tileCombinations(length):
    ways = [0] * (length + 1)
    ways[0] = 1

    for total in range(1, length + 1):
        for tile_size in (1, 2, 3, 4):
            if total >= tile_size:
                ways[total] += ways[total - tile_size]

    return ways[length]


def runTests():
    assert tileCombinations(5) == 15


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = tileCombinations(50)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
