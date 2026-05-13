import time
from itertools import combinations


def nCk(n, k):
    if k < 0 or k > n:
        return 0

    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def pointDigits():
    digits = []
    for point in range(81):
        x = point
        current = []
        for _ in range(4):
            current.append(x % 3)
            x //= 3
        digits.append(current)
    return digits


def buildGeometry():
    digits = pointDigits()

    def pointKey(values):
        return values[0] + 3 * values[1] + 9 * values[2] + 27 * values[3]

    def thirdPoint(a, b):
        return pointKey([-(digits[a][i] + digits[b][i]) % 3 for i in range(4)])

    negKey = [0] * 81
    for key in range(81):
        x = key
        values = []
        for _ in range(4):
            values.append((2 * (x % 3)) % 3)
            x //= 3
        negKey[key] = pointKey(values)

    directionIndex = {}
    for key in range(1, 81):
        canon = min(key, negKey[key])
        if canon not in directionIndex:
            directionIndex[canon] = len(directionIndex)

    lines = set()
    for a, b in combinations(range(81), 2):
        c = thirdPoint(a, b)
        lines.add(tuple(sorted((a, b, c))))

    lineMasks = []
    lineDirections = []

    for a, b, c in sorted(lines):
        lineMasks.append((1 << a) | (1 << b) | (1 << c))
        direction = pointKey([(digits[b][i] - digits[a][i]) % 3 for i in range(4)])
        canon = min(direction, negKey[direction])
        lineDirections.append(directionIndex[canon])

    assert len(lineMasks) == 1080
    return lineMasks, lineDirections


def computeUnionCounts(lineMasks, lineDirections):
    pairMasks = [[] for _ in range(4)]

    for i, maskI in enumerate(lineMasks):
        directionI = lineDirections[i]
        for j, maskJ in enumerate(lineMasks):
            if i == j:
                pairMasks[0].append(maskI)
            elif maskI & maskJ:
                pairMasks[1].append(maskI | maskJ)
            elif directionI == lineDirections[j]:
                pairMasks[2].append(maskI | maskJ)
            else:
                pairMasks[3].append(maskI | maskJ)

    pairUnionSizes = [3, 5, 6, 6]
    representatives = [classMasks[0] for classMasks in pairMasks]
    unionCounts = [0] * 13

    for classA in range(4):
        representative = representatives[classA]
        countA = len(pairMasks[classA])
        sizeA = pairUnionSizes[classA]

        for classB in range(4):
            intersections = [0] * 7
            for mask in pairMasks[classB]:
                intersections[(representative & mask).bit_count()] += 1

            sizeB = pairUnionSizes[classB]
            for intersectionSize, count in enumerate(intersections):
                unionSize = sizeA + sizeB - intersectionSize
                unionCounts[unionSize] += countA * count

    assert sum(unionCounts) == 1080 ** 4
    return unionCounts


def FFromUnionCounts(unionCounts, n):
    total = 0
    for unionSize, count in enumerate(unionCounts):
        total += count * nCk(81 - unionSize, n - unionSize)
    return total


def buildUnionCounts():
    return computeUnionCounts(*buildGeometry())


def runTests(unionCounts):
    assert FFromUnionCounts(unionCounts, 3) == 1080
    assert FFromUnionCounts(unionCounts, 6) == 159_690_960


if __name__ == "__main__":
    start = time.time()
    counts = buildUnionCounts()
    runTests(counts)
    answer = FFromUnionCounts(counts, 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
