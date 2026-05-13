import heapq
import math
import time


TARGET = 3_000_000


def generatedSequenceLength(x, y):
    terms = 1
    value = y
    modulus = x
    while value not in (0, 1):
        value = value * value % modulus
        modulus += 1
        terms += 1
    return terms


def initialActiveValues(x):
    if x <= 2:
        return []

    seen = bytearray(x)
    active = []
    value = 4 % x
    delta = 5

    for y in range(2, x // 2 + 1):
        if value > 1 and not seen[value]:
            seen[value] = 1
            active.append(value)

        value += delta
        if value >= x:
            value -= x
            if value >= x:
                value %= x
        delta += 2

    return active


def nextActiveWithMarker(active, modulus):
    seen = bytearray(modulus)
    nextActive = []
    for value in active:
        newValue = value * value % modulus
        if newValue > 1 and not seen[newValue]:
            seen[newValue] = 1
            nextActive.append(newValue)
    return nextActive


def nextActiveWithSet(active, modulus):
    nextActive = set()
    for value in active:
        newValue = value * value % modulus
        if newValue > 1:
            nextActive.add(newValue)
    return list(nextActive)


def maximumLengthForStart(x, markerThreshold=100_000):
    if x < 2:
        return 0
    if x == 2:
        return 1

    active = initialActiveValues(x)
    length = 2
    modulus = x + 1

    while len(active) > 1:
        if len(active) >= markerThreshold:
            active = nextActiveWithMarker(active, modulus)
        else:
            active = nextActiveWithSet(active, modulus)

        length += 1
        modulus += 1
        if not active:
            return length

    if not active:
        return length

    value = active[0]
    while value not in (0, 1):
        value = value * value % modulus
        length += 1
        modulus += 1

    return length


def maxSequenceLength(limit, targetPoints=16):
    if limit < 2:
        return 0

    cache = {}

    def g(x):
        if x not in cache:
            cache[x] = maximumLengthForStart(x)
        return cache[x]

    targetPoints = max(2, targetPoints)
    step = max(1, (limit - 2) // (targetPoints - 1))
    if step > 1:
        power = 10 ** int(math.log10(step))
        for multiple in (1, 2, 5, 10):
            if multiple * power >= step:
                step = multiple * power
                break

    points = list(range(2, limit + 1, step))
    if points[-1] != limit:
        points.append(limit)

    best = 0
    values = {}
    for point in points:
        value = g(point)
        values[point] = value
        if value > best:
            best = value

    heap = []
    for index in range(1, len(points)):
        left = points[index - 1]
        right = points[index]
        rightValue = values[right]
        bound = rightValue + (right - left)
        heapq.heappush(heap, (-bound, left, right, rightValue))

    while heap:
        bound = -heap[0][0]
        if bound <= best:
            break

        _, left, right, rightValue = heapq.heappop(heap)
        if right - left <= 1:
            continue

        middle = (left + right) // 2
        middleValue = g(middle)
        if middleValue > best:
            best = middleValue

        if middle - left > 1:
            leftBound = middleValue + (middle - left)
            if leftBound > best:
                heapq.heappush(heap, (-leftBound, left, middle, middleValue))

        if right - middle > 1:
            rightBound = rightValue + (right - middle)
            if rightBound > best:
                heapq.heappush(heap, (-rightBound, middle, right, rightValue))

    return best


def runTests():
    assert generatedSequenceLength(5, 3) == 29
    assert maximumLengthForStart(5) == 29
    assert maxSequenceLength(100) == 145
    assert maxSequenceLength(10_000) == 8_824


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maxSequenceLength(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
