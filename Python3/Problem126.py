import time


def layerCubeCount(x, y, z, layer):
    return 2 * (x * y + x * z + y * z) + 4 * (layer - 1) * (x + y + z + layer - 2)


def layerCounts(limit):
    counts = [0] * (limit + 1)
    x = 1

    while layerCubeCount(x, x, x, 1) <= limit:
        y = x
        while layerCubeCount(x, y, y, 1) <= limit:
            z = y
            while layerCubeCount(x, y, z, 1) <= limit:
                layer = 1
                while True:
                    cubes = layerCubeCount(x, y, z, layer)
                    if cubes > limit:
                        break
                    counts[cubes] += 1
                    layer += 1
                z += 1
            y += 1
        x += 1

    return counts


def leastLayerCountValue(target):
    limit = 200

    while True:
        counts = layerCounts(limit)
        for value, count in enumerate(counts):
            if count == target:
                return value
        limit *= 2


def runTests():
    counts = layerCounts(200)
    assert counts[22] == 2
    assert counts[46] == 4
    assert counts[78] == 5
    assert counts[118] == 8


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastLayerCountValue(1000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
