import math
import time


def generatedPoints(count):
    state = 290_797
    values = []
    for _ in range(2 * count):
        state = state * state % 50_515_093
        values.append(state % 2_000 - 1_000)
    return [(values[index], values[index + 1]) for index in range(0, len(values), 2)]


def canonicalLine(first, second):
    x1, y1 = first
    x2, y2 = second
    dx = x2 - x1
    dy = y2 - y1
    common = math.gcd(dx, dy)
    dx //= common
    dy //= common
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy
    a = dy
    b = -dx
    c = a * x1 + b * y1
    return a, b, c


def lineCountAndCrossedLineSum(point_count):
    points = generatedPoints(point_count)
    lines = set()
    for first_index in range(point_count):
        for second_index in range(first_index + 1, point_count):
            lines.add(canonicalLine(points[first_index], points[second_index]))
    slopes = {}
    for a, b, _ in lines:
        slopes[(a, b)] = slopes.get((a, b), 0) + 1
    line_count = len(lines)
    crossed_line_sum = line_count * line_count - sum(count * count for count in slopes.values())
    return line_count, crossed_line_sum


def crossedLineSum(point_count):
    return lineCountAndCrossedLineSum(point_count)[1]


def runTests():
    assert generatedPoints(3) == [(527, 144), (-488, 732), (-454, -947)]
    assert lineCountAndCrossedLineSum(3) == (3, 6)
    assert lineCountAndCrossedLineSum(100) == (4_948, 24_477_690)
    assert crossedLineSum(3) == 6
    assert crossedLineSum(100) == 24_477_690


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = crossedLineSum(2_500)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
