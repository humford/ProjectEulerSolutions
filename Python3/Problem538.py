from itertools import combinations
import time


def bitCountSequenceValue(n):
    return 2 ** ((3 * n).bit_count()) + 3 ** ((2 * n).bit_count()) + (n + 1).bit_count()


def quadrilateralScore(sides):
    perimeter = sum(sides)
    longest = max(sides)
    if 2 * longest >= perimeter:
        return None

    areaKey = 1
    for side in sides:
        areaKey *= perimeter - 2 * side
    return areaKey, perimeter


def maxQuadrilateralPerimeter(sequence):
    bestAreaKey = -1
    bestPerimeter = 0
    for sides in combinations(sequence, 4):
        score = quadrilateralScore(sides)
        if score is None:
            continue
        areaKey, perimeter = score
        if areaKey > bestAreaKey or (areaKey == bestAreaKey and perimeter > bestPerimeter):
            bestAreaKey = areaKey
            bestPerimeter = perimeter
    return bestPerimeter


def quadrilateralScan(stop, start=4):
    values = [bitCountSequenceValue(index) for index in range(1, stop + 1)]
    distinctValues = sorted(set(values))
    valueIndex = {value: index for index, value in enumerate(distinctValues)}
    counts = [0] * len(distinctValues)

    bestAreaKey = -1
    bestPerimeter = 0
    total = 0

    def bestForLargest(largestIndex):
        if counts[largestIndex] == 0:
            return None

        sides = [distinctValues[largestIndex]]
        needed = 3
        for index in range(largestIndex, -1, -1):
            available = counts[index] - (1 if index == largestIndex else 0)
            while available and needed:
                sides.append(distinctValues[index])
                available -= 1
                needed -= 1
            if needed == 0:
                break

        if needed:
            return None
        return quadrilateralScore(sides)

    for prefixLength, value in enumerate(values, 1):
        index = valueIndex[value]
        counts[index] += 1

        greaterElementCount = 0
        for largestIndex in range(index, len(distinctValues)):
            if largestIndex > index:
                greaterElementCount += counts[largestIndex]

            if largestIndex == index or greaterElementCount <= 3:
                score = bestForLargest(largestIndex)
                if score is None:
                    continue

                areaKey, perimeter = score
                if areaKey > bestAreaKey or (
                    areaKey == bestAreaKey and perimeter > bestPerimeter
                ):
                    bestAreaKey = areaKey
                    bestPerimeter = perimeter
            else:
                break

        if prefixLength >= start:
            total += bestPerimeter

    return total, bestPerimeter


def fOfPrefix(n):
    return quadrilateralScan(n)[1]


def quadrilateralSum(start, stop):
    return quadrilateralScan(stop, start)[0]


def runTests():
    assert bitCountSequenceValue(5) == 27
    assert [bitCountSequenceValue(index) for index in range(1, 11)] == [8, 9, 14, 9, 27, 16, 36, 9, 27, 28]
    assert maxQuadrilateralPerimeter([8, 9, 14, 9, 27]) == 59
    assert fOfPrefix(5) == 59
    assert fOfPrefix(10) == 118
    assert fOfPrefix(150) == 3_223
    assert quadrilateralSum(4, 150) == 234_761


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = quadrilateralSum(4, 3_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
