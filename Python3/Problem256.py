import math
import time

import numpy


TARGET = 200
SEARCH_LIMIT = 100000000


def tatamiFreeCounts(limit):
    counts = numpy.zeros(limit // 2, dtype=numpy.uint16)
    root = math.isqrt(limit - 1) + 1

    for width in range(7, root, 2):
        low = width + 3
        high = 2 * width - 4

        while low <= high and width * low < limit:
            capped_high = min(high, (limit - 1) // width)
            if capped_high >= low:
                start = width * low // 2
                stop = width * capped_high // 2
                counts[start : stop + 1 : width] += 1

            low += width + 1
            high += width - 1

    for width in range(8, root, 2):
        low = width + 3
        high = 2 * width - 4
        step = width // 2

        while low <= high and width * low < limit:
            capped_high = min(high, (limit - 1) // width)
            if capped_high >= low:
                start = width * low // 2
                stop = width * capped_high // 2
                counts[start : stop + 1 : step] += 1

            low += width + 1
            high += width - 1

    return counts


def smallestTatamiFreeRoomCount(target, limit):
    counts = tatamiFreeCounts(limit)
    matches = numpy.flatnonzero(counts == target)
    if len(matches) == 0:
        raise ValueError("search limit too small")
    return int(matches[0]) * 2


def runTests():
    counts = tatamiFreeCounts(2000)
    assert counts[70 // 2] == 1
    assert counts[1320 // 2] == 5
    assert int(numpy.flatnonzero(counts == 5)[0]) * 2 == 1320


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smallestTatamiFreeRoomCount(TARGET, SEARCH_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
