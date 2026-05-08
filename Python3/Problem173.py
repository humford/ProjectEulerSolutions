import time


def laminaeCount(tile_limit):
    count = 0
    outer = 3

    while 4 * (outer - 1) <= tile_limit:
        thickness = 1
        while 2 * thickness < outer:
            tiles = 4 * thickness * (outer - thickness)
            if tiles > tile_limit:
                break
            count += 1
            thickness += 1
        outer += 1

    return count


def runTests():
    assert laminaeCount(100) == 41


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = laminaeCount(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
