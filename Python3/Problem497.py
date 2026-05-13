import time


MODULUS = 10 ** 9
EDGES = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def expectedWalkDistance(start, target, width):
    if start == target:
        return 0
    if start < target:
        return (target - start) * (target + start - 2)
    return (start - target) * (2 * width - start - target)


def baseMoveCounts(modulus=None):
    counts = [[[[0] * 6 for _ in range(3)] for _ in range(3)] for _ in range(3)]

    for source in range(3):
        for target in range(3):
            if source == target:
                continue
            for start in range(3):
                vector = [0] * 6
                if start != source:
                    vector[EDGE_INDEX[(start, source)]] += 1
                vector[EDGE_INDEX[(source, target)]] += 1
                if modulus is not None:
                    vector = [value % modulus for value in vector]
                counts[source][target][start] = vector

    return counts


def advanceMoveCounts(counts, modulus=None):
    nextCounts = [[[[0] * 6 for _ in range(3)] for _ in range(3)] for _ in range(3)]

    for source in range(3):
        for target in range(3):
            if source == target:
                continue
            auxiliary = 3 - source - target

            for start in range(3):
                first = counts[source][auxiliary][start]
                second = counts[auxiliary][target][target]
                vector = [first[index] + second[index] for index in range(6)]
                vector[EDGE_INDEX[(auxiliary, source)]] += 1
                vector[EDGE_INDEX[(source, target)]] += 1

                if modulus is not None:
                    vector = [value % modulus for value in vector]
                nextCounts[source][target][start] = vector

    return nextCounts


def drunkenHanoiExpected(n, width, a, b, c):
    positions = [a, b, c]
    distances = [
        expectedWalkDistance(positions[source], positions[target], width)
        for source, target in EDGES
    ]

    counts = baseMoveCounts()
    for _ in range(2, n + 1):
        counts = advanceMoveCounts(counts)

    return sum(
        count * distance
        for count, distance in zip(counts[0][2][1], distances)
    )


def drunkenHanoiSum(limit):
    counts = baseMoveCounts(MODULUS)
    a = b = c = width = 1
    total = 0

    for n in range(1, limit + 1):
        a = a * 3 % MODULUS
        b = b * 6 % MODULUS
        c = c * 9 % MODULUS
        width = width * 10 % MODULUS

        if n > 1:
            counts = advanceMoveCounts(counts, MODULUS)

        distances = [
            (b - a) * (b + a - 2),
            (c - a) * (c + a - 2),
            (b - a) * (2 * width - b - a),
            (c - b) * (c + b - 2),
            (c - a) * (2 * width - c - a),
            (c - b) * (2 * width - c - b),
        ]
        distances = [distance % MODULUS for distance in distances]

        expected = 0
        for count, distance in zip(counts[0][2][1], distances):
            expected = (expected + count * distance) % MODULUS
        total = (total + expected) % MODULUS

    return total


def runTests():
    assert drunkenHanoiExpected(2, 5, 1, 3, 5) == 60
    assert drunkenHanoiExpected(3, 20, 4, 9, 17) == 2_358


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = drunkenHanoiSum(10_000) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
