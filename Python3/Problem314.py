import math
import time
from array import array


HALF_SIDE = 250


def squareRatio():
    return 250000.0 / 2000.0


def triangleCutRatio():
    area = 250000.0 - 4.0 * (75.0 * 75.0 / 2.0)
    perimeter = 4.0 * (500.0 - 2.0 * 75.0) + 4.0 * math.hypot(75.0, 75.0)
    return area / perimeter


def buildDistances(limit):
    distances = [[0.0] * (limit + 1) for _ in range(limit + 1)]

    for dx in range(limit + 1):
        row = distances[dx]
        for dy in range(limit + 1):
            row[dy] = math.hypot(dx, dy)

    return distances


def intersectionStart(a, scoreA, b, scoreB, dx, ratio, distances, limit):
    gap = b - a
    scoreGap = scoreB - scoreA

    if scoreGap >= 0.0:
        return b

    if scoreGap + ratio * gap <= 0.0:
        return limit + 1

    crossing = (scoreA - scoreB) / ratio
    denom = gap * gap - crossing * crossing
    offset = (-gap + crossing * math.sqrt(1.0 + (4.0 * dx * dx) / denom)) * 0.5
    start = int(b + offset)

    if start < b:
        start = b

    distanceRow = distances[dx]
    while start <= limit:
        candidateScore = scoreB - ratio * distanceRow[start - b]
        incumbentScore = scoreA - ratio * distanceRow[start - a]

        if candidateScore >= incumbentScore - 1e-13:
            break

        start += 1

    return start if start <= limit else limit + 1


def bestPathForRatio(limit, ratio, distances):
    negative = -1e300
    negativeHalf = negative / 2.0
    indices = range(limit + 1)

    dp = [array("d", [negative] * (limit + 1)) for _ in indices]
    parentX = [array("h", [-1] * (limit + 1)) for _ in indices]
    parentY = [array("h", [-1] * (limit + 1)) for _ in indices]

    for y in indices:
        dp[0][y] = -ratio * y

    for rightX in range(1, limit + 1):
        best = [negative] * (limit + 1)
        bestParentX = array("h", [-1] * (limit + 1))
        bestParentY = array("h", [-1] * (limit + 1))

        for leftX in range(rightX):
            dx = rightX - leftX
            halfDx = dx * 0.5
            previous = dp[leftX]
            distanceRow = distances[dx]
            sites = []
            values = []
            starts = []

            for y in indices:
                value = previous[y]
                if value <= negativeHalf:
                    continue

                adjusted = value + halfDx * y

                if not sites:
                    sites.append(y)
                    values.append(adjusted)
                    starts.append(y)
                    continue

                while sites:
                    start = intersectionStart(
                        sites[-1], values[-1], y, adjusted, dx, ratio, distances, limit
                    )

                    if start <= starts[-1]:
                        sites.pop()
                        values.pop()
                        starts.pop()

                        if not sites:
                            break
                    else:
                        break

                if not sites:
                    sites.append(y)
                    values.append(adjusted)
                    starts.append(y)
                else:
                    sites.append(y)
                    values.append(adjusted)
                    starts.append(start)

            envelopeIndex = 0
            envelopeLength = len(sites)

            for rightY in indices:
                while (
                    envelopeIndex + 1 < envelopeLength
                    and rightY >= starts[envelopeIndex + 1]
                ):
                    envelopeIndex += 1

                leftY = sites[envelopeIndex]
                if leftY > rightY:
                    continue

                score = (
                    values[envelopeIndex]
                    - ratio * distanceRow[rightY - leftY]
                    + halfDx * rightY
                )

                if score > best[rightY]:
                    best[rightY] = score
                    bestParentX[rightY] = leftX
                    bestParentY[rightY] = leftY

        dp[rightX] = array("d", best)
        parentX[rightX] = bestParentX
        parentY[rightX] = bestParentY

    path = []
    x = limit
    y = limit

    while x != 0:
        path.append((x, y))
        x, y = int(parentX[x][y]), int(parentY[x][y])

    path.append((0, y))
    path.reverse()

    area = 0.0
    perimeter = float(path[0][1])

    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        dx = x2 - x1
        dy = abs(y2 - y1)
        area += (y1 + y2) * dx * 0.5
        perimeter += distances[dx][dy]

    return area, perimeter


def optimalRatio(limit=HALF_SIDE):
    distances = buildDistances(limit)
    ratio = triangleCutRatio()

    for _ in range(12):
        area, perimeter = bestPathForRatio(limit, ratio, distances)
        newRatio = area / perimeter

        if abs(newRatio - ratio) < 5e-13:
            return newRatio

        ratio = newRatio

    return ratio


def runTests():
    assert abs(squareRatio() - 125.0) < 1e-12
    assert round(triangleCutRatio(), 2) == 130.87


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.8f}".format(optimalRatio())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
