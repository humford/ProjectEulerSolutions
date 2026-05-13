import math
import time
from collections import Counter


PROBLEM_LIMIT = 2_000_000


def firstPoints(count):
    x = y = 1
    points = []

    for _ in range(count):
        x = x * 1248 % 32323
        y = y * 8421 % 30103
        points.append((x - 16161, y - 15051))

    return points


def choose3(count):
    return count * (count - 1) * (count - 2) // 6


def containingTriangleCount(count):
    angles = []
    directions = Counter()
    x = y = 1

    for _ in range(count):
        x = x * 1248 % 32323
        y = y * 8421 % 30103
        pointX = x - 16161
        pointY = y - 15051
        angles.append(math.atan2(pointY, pointX))

        divisor = math.gcd(abs(pointX), abs(pointY))
        directions[(pointX // divisor, pointY // divisor)] += 1

    angles.sort()
    doubledAngles = angles + [angle + 2 * math.pi for angle in angles]
    outsideOrBoundary = 0
    end = 0

    # If all three rays lie in an open semicircle, the triangle cannot
    # contain the origin.  Exact antipodal boundary cases are subtracted below.
    for start in range(count):
        if end < start + 1:
            end = start + 1

        while (
            end < start + count
            and doubledAngles[end] - doubledAngles[start] < math.pi - 1e-14
        ):
            end += 1

        insideSemicircle = end - start - 1
        outsideOrBoundary += insideSemicircle * (insideSemicircle - 1) // 2

    total = choose3(count)
    candidateContaining = total - outsideOrBoundary

    boundaryTriangles = 0
    seen = set()

    for direction, forwardCount in directions.items():
        if direction in seen:
            continue

        opposite = (-direction[0], -direction[1])
        backwardCount = directions.get(opposite, 0)
        seen.add(direction)
        seen.add(opposite)

        if backwardCount:
            lineCount = forwardCount + backwardCount
            boundaryTriangles += forwardCount * backwardCount * (count - lineCount)
            boundaryTriangles += (
                choose3(lineCount) - choose3(forwardCount) - choose3(backwardCount)
            )

    return candidateContaining - boundaryTriangles


def runTests():
    assert firstPoints(8) == [
        (-14913, -6630),
        (-10161, 5625),
        (5226, 11896),
        (8340, -10778),
        (15852, -5203),
        (-15165, 11295),
        (-1427, -14495),
        (12407, 1060),
    ]
    assert containingTriangleCount(8) == 20
    assert containingTriangleCount(600) == 8_950_634
    assert containingTriangleCount(40_000) == 2_666_610_948_988


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = containingTriangleCount(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
