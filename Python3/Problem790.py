import sys
import time
from array import array


GRID_SIZE = 50_515_093
SEED = 290_797


def rectangles(count):
    s = SEED
    for _ in range(count):
        x1 = s
        s = s * s % GRID_SIZE
        x2 = s
        s = s * s % GRID_SIZE
        y1 = s
        s = s * s % GRID_SIZE
        y2 = s
        s = s * s % GRID_SIZE

        yield min(x1, x2), max(x1, x2) + 1, min(y1, y2), max(y1, y2) + 1


def C(t):
    if t == 0:
        return 12 * GRID_SIZE * GRID_SIZE

    xBoundaries = {0, GRID_SIZE}
    yBoundaries = {0, GRID_SIZE}
    events = []

    for xLow, xHigh, yLow, yHigh in rectangles(t):
        xBoundaries.add(xLow)
        xBoundaries.add(xHigh)
        yBoundaries.add(yLow)
        yBoundaries.add(yHigh)
        events.append((xLow, 1, yLow, yHigh))
        events.append((xHigh, 11, yLow, yHigh))

    xValues = sorted(xBoundaries)
    yValues = sorted(yBoundaries)
    yIndex = {value: index for index, value in enumerate(yValues)}
    events = [(x, shift, yIndex[yLow], yIndex[yHigh]) for x, shift, yLow, yHigh in events]
    events.sort()

    intervalCount = len(yValues) - 1
    treeSize = 4 * intervalCount + 5
    segment = array("Q", [0]) * (12 * treeSize)
    lazy = bytearray(treeSize)
    sys.setrecursionlimit(1_000_000)

    def build(node, left, right):
        base = 12 * node
        if right - left == 1:
            segment[base] = yValues[left + 1] - yValues[left]
            return

        middle = (left + right) // 2
        build(2 * node, left, middle)
        build(2 * node + 1, middle, right)
        segment[base] = segment[24 * node] + segment[24 * node + 12]

    build(1, 0, intervalCount)
    rotationBuffer = [0] * 12

    def applyRotation(node, shift):
        shift %= 12
        if shift == 0:
            return

        base = 12 * node
        if shift == 1:
            value = segment[base + 11]
            for i in range(11, 0, -1):
                segment[base + i] = segment[base + i - 1]
            segment[base] = value
        elif shift == 11:
            value = segment[base]
            for i in range(11):
                segment[base + i] = segment[base + i + 1]
            segment[base + 11] = value
        else:
            for i in range(12):
                rotationBuffer[i] = segment[base + (i - shift) % 12]
            for i in range(12):
                segment[base + i] = rotationBuffer[i]

        value = lazy[node] + shift
        lazy[node] = value - 12 if value >= 12 else value

    def push(node):
        shift = lazy[node]
        if shift:
            applyRotation(2 * node, shift)
            applyRotation(2 * node + 1, shift)
            lazy[node] = 0

    def pull(node):
        base = 12 * node
        leftBase = 24 * node
        rightBase = leftBase + 12
        for i in range(12):
            segment[base + i] = segment[leftBase + i] + segment[rightBase + i]

    def update(node, left, right, queryLeft, queryRight, shift):
        if queryLeft <= left and right <= queryRight:
            applyRotation(node, shift)
            return

        push(node)
        middle = (left + right) // 2
        if queryLeft < middle:
            update(2 * node, left, middle, queryLeft, queryRight, shift)
        if queryRight > middle:
            update(2 * node + 1, middle, right, queryLeft, queryRight, shift)
        pull(node)

    counts = [0] * 12
    eventIndex = 0
    eventCount = len(events)

    for index in range(len(xValues) - 1):
        x = xValues[index]
        while eventIndex < eventCount and events[eventIndex][0] == x:
            _, shift, yLow, yHigh = events[eventIndex]
            update(1, 0, intervalCount, yLow, yHigh, shift)
            eventIndex += 1

        width = xValues[index + 1] - x
        if width:
            base = 12
            for residue in range(12):
                counts[residue] += width * segment[base + residue]

    total = 12 * counts[0]
    for hour in range(1, 12):
        total += hour * counts[hour]
    return total


def runTests():
    assert C(0) == 30_621_295_449_583_788
    assert C(1) == 30_613_048_345_941_659
    assert C(10) == 21_808_930_308_198_471
    assert C(100) == 16_190_667_393_984_172


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = C(10 ** 5)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
