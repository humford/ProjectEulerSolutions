import math
import time
from collections import defaultdict


LIMIT = 10**6


def integerLadderTriplets(limit):
    heights_by_width = defaultdict(list)
    m = 2

    while m * m + 1 < limit:
        for n in range(1, m):
            if (m - n) % 2 == 0 or math.gcd(m, n) != 1:
                continue

            first_leg = m * m - n * n
            second_leg = 2 * m * n
            hypotenuse = m * m + n * n

            if hypotenuse >= limit:
                continue

            scale = 1
            while scale * hypotenuse < limit:
                heights_by_width[scale * first_leg].append(scale * second_leg)
                heights_by_width[scale * second_leg].append(scale * first_leg)
                scale += 1

        m += 1

    total = 0

    for heights in heights_by_width.values():
        heights.sort()

        for i, first_height in enumerate(heights):
            for second_height in heights[i + 1 :]:
                if first_height * second_height % (first_height + second_height) == 0:
                    total += 1

    return total


def runTests():
    assert integerLadderTriplets(200) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = integerLadderTriplets(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
