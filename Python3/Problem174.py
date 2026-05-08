import time


def laminaeTypeCount(tile_limit, max_arrangements):
    counts = [0] * (tile_limit + 1)
    outer = 3

    while 4 * (outer - 1) <= tile_limit:
        thickness = 1
        while 2 * thickness < outer:
            tiles = 4 * thickness * (outer - thickness)
            if tiles > tile_limit:
                break
            counts[tiles] += 1
            thickness += 1
        outer += 1

    return sum(1 for count in counts if 1 <= count <= max_arrangements)


def runTests():
    assert laminaeTypeCount(1000, 10) == 249


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = laminaeTypeCount(1000000, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
