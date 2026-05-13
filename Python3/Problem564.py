import time
from functools import lru_cache
from math import asin, comb, factorial, pi, sqrt


MAX_N = 50
FACTORIALS = [factorial(i) for i in range(MAX_N + 1)]


def extraPartCounts(total, maxPart=None):
    if total == 0:
        yield {}
        return
    if maxPart is None or maxPart > total:
        maxPart = total
    for part in range(maxPart, 0, -1):
        for rest in extraPartCounts(total - part, part):
            counts = dict(rest)
            counts[part] = counts.get(part, 0) + 1
            yield counts


def sideCountMap(n, extraCounts):
    counts = {1: n - sum(extraCounts.values())}
    for extra, count in extraCounts.items():
        counts[extra + 1] = count
    return tuple(sorted(counts.items()))


def orderedSplitCount(n, extraCounts):
    denominator = FACTORIALS[n - sum(extraCounts.values())]
    for count in extraCounts.values():
        denominator *= FACTORIALS[count]
    return FACTORIALS[n] // denominator


def signedTriangleSum(radius, sideCounts, skipSide=None):
    total = 0.0
    for side, count in sideCounts:
        if side == skipSide:
            continue
        total += count * side * sqrt(max(0.0, 4 * radius * radius - side * side))
    return total


def maximalPolygonArea(sideCounts):
    maxSide = max(side for side, count in sideCounts)
    minRadius = maxSide / 2
    angleAtMinRadius = sum(
        count * (pi if side == maxSide else 2 * asin(side / maxSide))
        for side, count in sideCounts
    )

    if angleAtMinRadius >= 2 * pi:
        def excessAngle(radius):
            return (
                sum(count * 2 * asin(side / (2 * radius)) for side, count in sideCounts)
                - 2 * pi
            )

        low = minRadius
        high = minRadius
        while excessAngle(high) > 0:
            high *= 2
        for _ in range(55):
            middle = (low + high) / 2
            if excessAngle(middle) > 0:
                low = middle
            else:
                high = middle
        radius = (low + high) / 2
        return 0.25 * signedTriangleSum(radius, sideCounts)

    def dominantSideImbalance(radius):
        dominantAngle = 2 * asin(maxSide / (2 * radius))
        otherAngles = sum(
            count * 2 * asin(side / (2 * radius))
            for side, count in sideCounts
            if side != maxSide
        )
        return dominantAngle - otherAngles

    low = minRadius
    high = minRadius
    while dominantSideImbalance(high) > 0:
        high *= 2
    for _ in range(55):
        middle = (low + high) / 2
        if dominantSideImbalance(middle) > 0:
            low = middle
        else:
            high = middle
    radius = (low + high) / 2
    return 0.25 * (
        signedTriangleSum(radius, sideCounts, skipSide=maxSide)
        - maxSide * sqrt(max(0.0, 4 * radius * radius - maxSide * maxSide))
    )


@lru_cache(maxsize=None)
def expectedArea(n):
    splitCount = comb(2 * n - 4, n - 1)
    weightedArea = 0.0
    for extraCounts in extraPartCounts(n - 3):
        sideCounts = sideCountMap(n, extraCounts)
        weightedArea += orderedSplitCount(n, extraCounts) * maximalPolygonArea(sideCounts)
    return weightedArea / splitCount


def maximalPolygonAreaSum(k):
    return sum(expectedArea(n) for n in range(3, k + 1))


def rounded(value):
    return f"{value:.6f}"


def runTests():
    assert rounded(expectedArea(3)) == "0.433013"
    assert rounded(expectedArea(4)) == "1.299038"
    assert rounded(maximalPolygonAreaSum(3)) == "0.433013"
    assert rounded(maximalPolygonAreaSum(4)) == "1.732051"
    assert rounded(maximalPolygonAreaSum(5)) == "4.604767"
    assert rounded(maximalPolygonAreaSum(10)) == "66.955511"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rounded(maximalPolygonAreaSum(50))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
