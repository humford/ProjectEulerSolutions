import bisect
import math
import time


MOD_RANDOM = 50_515_093


def generatePoints(count):
    value = 290_797
    points = []

    for _ in range(count):
        x = value
        value = value * value % MOD_RANDOM
        y = value
        value = value * value % MOD_RANDOM
        points.append((x, y))

    return points


def squaredDistance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def initialBest(points, sampleSize=512):
    sampleSize = min(sampleSize, len(points))
    best = None

    for i in range(sampleSize):
        for j in range(i + 1, sampleSize):
            distance = squaredDistance(points[i], points[j])
            if best is None or distance < best:
                best = distance

    return best


def closestSquaredDistance(points):
    points = sorted(points)
    best = initialBest(points)
    active = []
    left = 0

    for point in points:
        x, y = point

        while left < len(points):
            dx = x - points[left][0]
            if dx * dx <= best:
                break
            oldX, oldY = points[left]
            index = bisect.bisect_left(active, (oldY, oldX))
            active.pop(index)
            left += 1

        band = math.isqrt(best) + 1
        lo = bisect.bisect_left(active, (y - band, -1))
        hi = bisect.bisect_right(active, (y + band, MOD_RANDOM + 1))

        for otherY, otherX in active[lo:hi]:
            distance = squaredDistance(point, (otherX, otherY))
            if distance < best:
                best = distance

        bisect.insort(active, (y, x))

    return best


def d(k):
    return math.sqrt(closestSquaredDistance(generatePoints(k)))


def formattedD(k):
    return f"{d(k):.9f}"


def runTests():
    assert formattedD(14) == "546446.466846479"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedD(2_000_000)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
