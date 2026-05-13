from bisect import bisect_left
from collections import defaultdict
import time


ROBOT_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)


def smoothNumbers(limit):
    values = []

    def generate(index, current):
        if index == len(ROBOT_PRIMES):
            values.append(current)
            return

        prime = ROBOT_PRIMES[index]
        while current <= limit:
            generate(index + 1, current)
            current *= prime

    generate(0, 1)
    return sorted(values)


def minimalAreasUpTo(maxVariants):
    sideLimit = 100_000

    while True:
        sides = smoothNumbers(sideLimit)
        variantCounts = defaultdict(int)

        for upperIndex, longerSide in enumerate(sides):
            lowerBound = (10 * longerSide + 10) // 11
            lowerIndex = bisect_left(sides, lowerBound, 0, upperIndex + 1)
            for shorterSide in sides[lowerIndex : upperIndex + 1]:
                variantCounts[shorterSide * longerSide] += 1

        best = {}
        for area, variants in variantCounts.items():
            if 2 <= variants <= maxVariants and (
                variants not in best or area < best[variants]
            ):
                best[variants] = area

        if len(best) == maxVariants - 1 and max(best.values()) * 11 <= 10 * sideLimit * sideLimit:
            return best

        sideLimit *= 10


def minimalArea(variants):
    return minimalAreasUpTo(variants)[variants]


def robotWelderSum():
    areas = minimalAreasUpTo(100)
    return sum(areas[variants] for variants in range(2, 101))


def runTests():
    assert smoothNumbers(25) == [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
    ]
    assert minimalArea(3) == 889_200


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = robotWelderSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
