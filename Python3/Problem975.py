import math
import time


TARGET_MIN = 500
TARGET_MAX = 1000


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0

    for prime in range(2, int(limit**0.5) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )

    return [value for value in range(limit + 1) if sieve[value]]


def criticalZValues(a, b):
    total = a + b
    difference = abs(a - b)
    sineCount = total // 2 + 1
    cosineCount = difference // 2
    sineIndex = 0
    cosineIndex = 0
    values = []
    previousNumerator = None
    previousDenominator = None

    while sineIndex < sineCount or cosineIndex < cosineCount:
        if cosineIndex == cosineCount:
            numerator, denominator, family, index = 2 * sineIndex, total, 0, sineIndex
            sineIndex += 1
        elif sineIndex == sineCount:
            numerator, denominator, family, index = (
                2 * cosineIndex + 1,
                difference,
                1,
                cosineIndex,
            )
            cosineIndex += 1
        else:
            sineNumerator, sineDenominator = 2 * sineIndex, total
            cosineNumerator, cosineDenominator = 2 * cosineIndex + 1, difference
            left = sineNumerator * cosineDenominator
            right = cosineNumerator * sineDenominator

            if left < right:
                numerator, denominator, family, index = (
                    sineNumerator,
                    sineDenominator,
                    0,
                    sineIndex,
                )
                sineIndex += 1
            elif left > right:
                numerator, denominator, family, index = (
                    cosineNumerator,
                    cosineDenominator,
                    1,
                    cosineIndex,
                )
                cosineIndex += 1
            else:
                numerator, denominator, family, index = (
                    sineNumerator,
                    sineDenominator,
                    0,
                    sineIndex,
                )
                sineIndex += 1
                cosineIndex += 1

        if (
            previousNumerator is not None
            and previousNumerator * denominator == numerator * previousDenominator
        ):
            continue
        previousNumerator, previousDenominator = numerator, denominator

        if family == 0:
            z = 0.5 - 0.5 * math.cos((2.0 * math.pi * a * index) / total)
        else:
            z = 0.5 - (difference / (2.0 * total)) * math.cos(
                (math.pi * a * (2 * index + 1)) / difference
            )
        values.append(z)

    return values


def F(a, b, c, d):
    xValues = criticalZValues(a, b)
    yValues = criticalZValues(c, d)
    xCells = len(xValues) - 1
    yCells = len(yValues) - 1
    endCorner = ("corner", xCells, yCells)
    epsilon = 1e-16

    def sign(value):
        if value > epsilon:
            return 1
        if value < -epsilon:
            return -1
        return 0

    def addPoint(points, point):
        if point not in points:
            points.append(point)
        if len(points) > 2:
            raise RuntimeError("Degenerate cell with too many boundary points.")

    def cellSegment(i, j):
        zx0 = xValues[i]
        zx1 = xValues[i + 1]
        zy0 = yValues[j]
        zy1 = yValues[j + 1]
        differences = (
            zx0 - zy0,
            zx1 - zy0,
            zx0 - zy1,
            zx1 - zy1,
        )
        s00, s10, s01, s11 = [sign(value) for value in differences]
        points = []

        if s00 == 0:
            addPoint(points, ("corner", i, j))
        if s01 == 0:
            addPoint(points, ("corner", i, j + 1))
        if s00 != 0 and s01 != 0 and s00 != s01:
            addPoint(points, ("x", i, j))

        if s10 == 0:
            addPoint(points, ("corner", i + 1, j))
        if s11 == 0:
            addPoint(points, ("corner", i + 1, j + 1))
        if s10 != 0 and s11 != 0 and s10 != s11:
            addPoint(points, ("x", i + 1, j))

        if s00 == 0:
            addPoint(points, ("corner", i, j))
        if s10 == 0:
            addPoint(points, ("corner", i + 1, j))
        if s00 != 0 and s10 != 0 and s00 != s10:
            addPoint(points, ("y", j, i))

        if s01 == 0:
            addPoint(points, ("corner", i, j + 1))
        if s11 == 0:
            addPoint(points, ("corner", i + 1, j + 1))
        if s01 != 0 and s11 != 0 and s01 != s11:
            addPoint(points, ("y", j + 1, i))

        if not points:
            return None
        if len(points) != 2:
            raise RuntimeError("Degenerate cell with only one boundary point.")
        return tuple(points)

    def pointZ(point):
        if point[0] == "x":
            return xValues[point[1]]
        if point[0] == "y":
            return yValues[point[1]]
        return 0.5 * (xValues[point[1]] + yValues[point[2]])

    def nextCellAcrossEdge(cell, point):
        i, j = cell
        if point[0] == "x":
            ix, jy = point[1], point[2]
            return (ix, jy) if cell == (ix - 1, jy) else (ix - 1, jy)

        jy, ix = point[1], point[2]
        return (ix, jy) if cell == (ix, jy - 1) else (ix, jy - 1)

    def chooseNextCellAtCorner(corner, fromCell, previousPoint):
        ix, jy = corner[1], corner[2]
        for deltaI in (-1, 0):
            for deltaJ in (-1, 0):
                candidate = (ix + deltaI, jy + deltaJ)
                ci, cj = candidate
                if not (0 <= ci < xCells and 0 <= cj < yCells):
                    continue
                if candidate == fromCell:
                    continue

                segment = cellSegment(ci, cj)
                if segment is None or corner not in segment:
                    continue
                other = segment[0] if segment[1] == corner else segment[1]
                if other != previousPoint:
                    return candidate

        return fromCell

    cell = (0, 0)
    point = ("corner", 0, 0)
    previousPoint = None
    totalVariation = 0.0

    for _ in range(4 * xCells * yCells + 10):
        if point == endCorner:
            return totalVariation

        segment = cellSegment(cell[0], cell[1])
        if segment is None:
            raise RuntimeError("Lost the curve.")

        if point == segment[0]:
            nextPoint = segment[1]
        elif point == segment[1]:
            nextPoint = segment[0]
        elif point[0] == "corner":
            ix, jy = point[1], point[2]
            found = None
            for deltaI in (-1, 0):
                for deltaJ in (-1, 0):
                    candidate = (ix + deltaI, jy + deltaJ)
                    ci, cj = candidate
                    if not (0 <= ci < xCells and 0 <= cj < yCells):
                        continue
                    segment = cellSegment(ci, cj)
                    if segment is None or point not in segment:
                        continue
                    other = segment[0] if segment[1] == point else segment[1]
                    if previousPoint is not None and other == previousPoint:
                        continue
                    found = (candidate, other)
                    break
                if found:
                    break
            if found is None:
                raise RuntimeError("Corner relocation failed.")
            cell, nextPoint = found
        else:
            raise RuntimeError("Point is not on the expected segment.")

        totalVariation += abs(pointZ(nextPoint) - pointZ(point))

        if nextPoint[0] == "corner":
            cell = chooseNextCellAtCorner(nextPoint, cell, point)
        else:
            cell = nextCellAcrossEdge(cell, nextPoint)
        previousPoint, point = point, nextPoint

    raise RuntimeError("Exceeded path traversal bound.")


def G(lower, upper):
    primes = [prime for prime in primesUpTo(upper) if prime >= lower]
    total = 0.0
    for index, p in enumerate(primes):
        for q in primes[index + 1 :]:
            total += F(p, q, p, 2 * q - p)
    return total


def solve():
    return G(TARGET_MIN, TARGET_MAX)


def runTests():
    assert abs(F(3, 5, 3, 7) - 7.01772) < 1e-5
    assert abs(F(7, 17, 9, 19) - 26.79578) < 1e-5
    assert abs(G(3, 20) - 463.80866) < 1e-5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + format(answer, ".5f") + " in " + str(elapsed) + " seconds.")
