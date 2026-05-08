import time


def replacementsForTile(length, tile_size):
    ways = [0] * (length + 1)
    ways[0] = 1

    for total in range(1, length + 1):
        ways[total] = ways[total - 1]
        if total >= tile_size:
            ways[total] += ways[total - tile_size]

    return ways[length] - 1


def totalReplacements(length):
    return sum(replacementsForTile(length, tile_size) for tile_size in (2, 3, 4))


def runTests():
    assert totalReplacements(5) == 12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totalReplacements(50)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
