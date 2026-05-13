import bisect
import math
import time


def primeSieve(limit):
    isPrime = [True] * (limit + 1)
    isPrime[0] = False
    isPrime[1] = False

    for number in range(2, math.isqrt(limit) + 1):
        if isPrime[number]:
            for multiple in range(number * number, limit + 1, number):
                isPrime[multiple] = False

    return [number for number in range(limit + 1) if isPrime[number]]


def gapAsFloat(gap):
    return float(gap)


def jumpSumValue(p, gap, distance):
    gap = gapAsFloat(gap)
    distance = float(distance)
    jumpLength = 1 / math.sqrt(p)
    position = 0.0
    jumpCount = 0

    while True:
        jumpCount += 1
        position = (position + jumpLength) % 1.0
        if distance <= position <= distance + gap:
            return jumpCount * jumpLength


def jumpSum(p, gap, distance):
    return "{:.4f}".format(jumpSumValue(p, gap, distance))


def maximumGap(points):
    sortedPoints = sorted(points)
    best = sortedPoints[0] + 1.0 - sortedPoints[-1]

    for index in range(len(sortedPoints) - 1):
        gap = sortedPoints[index + 1] - sortedPoints[index]
        if gap > best:
            best = gap

    return best


def orbitPointsUntilCovered(p, gap):
    jumpLength = 1 / math.sqrt(p)
    points = []
    position = 0.0

    while True:
        for _ in range(10_000):
            position = (position + jumpLength) % 1.0
            points.append(position)

        if maximumGap(points) <= gap:
            return points


def find(parent, index):
    while parent[index] != index:
        parent[index] = parent[parent[index]]
        index = parent[index]
    return index


def firstHitSegments(p, gap):
    points = orbitPointsUntilCovered(p, gap)
    domainEnd = 1.0 - gap
    intervals = []
    coordinates = [0.0, domainEnd]

    for jumpCount, position in enumerate(points, 1):
        lower = max(0.0, position - gap)
        upper = min(position, domainEnd)

        if upper > lower:
            intervals.append((lower, upper, jumpCount))
            coordinates.append(lower)
            coordinates.append(upper)

    coordinates = sorted(set(coordinates))
    cellCount = len(coordinates) - 1
    parent = list(range(cellCount + 1))
    firstHits = [0] * cellCount
    assigned = 0

    for lower, upper, jumpCount in intervals:
        left = bisect.bisect_left(coordinates, lower)
        right = bisect.bisect_left(coordinates, upper)
        index = find(parent, left)

        while index < right:
            firstHits[index] = jumpCount
            parent[index] = find(parent, index + 1)
            assigned += 1
            index = find(parent, index)

        if assigned == cellCount:
            break

    jumpLength = 1 / math.sqrt(p)
    segments = []
    start = coordinates[0]
    currentHit = firstHits[0]

    for index in range(1, cellCount):
        if firstHits[index] != currentHit:
            segments.append((start, coordinates[index], currentHit * jumpLength))
            start = coordinates[index]
            currentHit = firstHits[index]

    segments.append((start, coordinates[cellCount], currentHit * jumpLength))
    return segments


def maxJumpSumValue(limit, gap):
    gap = gapAsFloat(gap)
    events = []

    for prime in primeSieve(limit):
        for start, end, value in firstHitSegments(prime, gap):
            events.append((start, value))
            events.append((end, -value))

    events.sort(key=lambda event: event[0])
    current = 0.0
    best = 0.0
    index = 0

    while index < len(events):
        position = events[index][0]

        while index < len(events) and events[index][0] == position:
            current += events[index][1]
            index += 1

        if index < len(events) and events[index][0] > position and current > best:
            best = current

    return best


def maxJumpSum(limit, gap):
    return "{:.4f}".format(maxJumpSumValue(limit, gap))


def runTests():
    assert jumpSum(2, "0.06", "0.7") == "0.7071"
    assert jumpSum(2, "0.06", "0.3543") == "1.4142"
    assert 16.2634 < jumpSumValue(2, "0.06", "0.2427") < 16.2635
    assert maxJumpSum(3, "0.06") == "29.5425"
    assert maxJumpSum(10, "0.01") == "266.9010"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maxJumpSum(100, "0.00002")
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
