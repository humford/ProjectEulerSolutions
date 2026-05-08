import math
import time
from array import array


def perimeterSolutionCounts(limit):
    counts = array("H", [0]) * (limit + 1)
    max_m = int((limit // 2) ** 0.5) + 1

    for m in range(2, max_m + 1):
        for n in range(1, m):
            if (m + n) % 2 == 0 or math.gcd(m, n) != 1:
                continue

            primitive_perimeter = 2 * m * (m + n)
            if primitive_perimeter > limit:
                break

            for perimeter in range(primitive_perimeter, limit + 1, primitive_perimeter):
                counts[perimeter] += 1

    return counts


def singularTriangleCount(limit):
    return perimeterSolutionCounts(limit).count(1)


def runTests():
    counts = perimeterSolutionCounts(120)
    assert counts[120] == 3
    assert singularTriangleCount(50) == 6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = singularTriangleCount(1500000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
