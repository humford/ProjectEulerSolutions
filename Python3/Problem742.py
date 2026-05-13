import heapq
import math
import time


def primitivePairs(limit):
    pairs = []
    for x in range(1, limit + 1):
        xSquared = x * x
        for y in range(1, limit + 1):
            if math.gcd(x, y) == 1:
                pairs.append((x, y, xSquared, y * y))
    return pairs


def smallestPairsByWeight(pairs, count, weightRatio):
    heap = []
    for x, y, xSquared, ySquared in pairs:
        weight = xSquared + weightRatio * ySquared
        tieBreaker = x + y
        item = (-weight, -tieBreaker, -x, -y, x, y)
        if len(heap) < count:
            heapq.heappush(heap, item)
        elif item > heap[0]:
            heapq.heapreplace(heap, item)

    return [(item[4], item[5]) for item in heap]


def sortBySlope(vectors):
    return sorted(vectors, key=lambda vector: (vector[1] / vector[0], vector[0], vector[1]))


def areaFromHalfEdges(edges):
    prefixX = 0
    prefixY = 0
    area = 0
    for deltaX, deltaY in edges:
        area += prefixX * deltaY - prefixY * deltaX
        prefixX += deltaX
        prefixY += deltaY
    return area


def polygonAreaFromInteriorDirections(interiorDirections):
    directions = sortBySlope(interiorDirections)
    halfEdges = [(1, 0)]
    halfEdges.extend(directions)
    halfEdges.append((0, 1))
    halfEdges.extend([(-x, y) for x, y in reversed(directions)])
    return areaFromHalfEdges(halfEdges)


def minimumSymmetricPolygonArea(vertices):
    if vertices < 4 or vertices % 4 != 0:
        raise ValueError("vertices must be a positive multiple of 4")

    interiorCount = (vertices - 4) // 4
    if interiorCount == 0:
        return 1

    limit = 40
    pairs = primitivePairs(limit)
    bestArea = None

    for ratioNumerator in range(1, 1001):
        weightRatio = ratioNumerator / 1000.0

        while True:
            chosen = smallestPairsByWeight(pairs, interiorCount, weightRatio)
            maxX = max(x for x, _ in chosen)
            maxY = max(y for _, y in chosen)
            if maxX < limit and maxY < limit:
                break
            limit *= 2
            pairs = primitivePairs(limit)

        area = polygonAreaFromInteriorDirections(chosen)
        if bestArea is None or area < bestArea:
            bestArea = area

    return bestArea


def runTests():
    assert minimumSymmetricPolygonArea(4) == 1
    assert minimumSymmetricPolygonArea(8) == 7
    assert minimumSymmetricPolygonArea(40) == 1_039
    assert minimumSymmetricPolygonArea(100) == 17_473


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimumSymmetricPolygonArea(1_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
