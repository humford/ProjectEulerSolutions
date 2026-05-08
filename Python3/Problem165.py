import math
import time


def generatedSegments(count):
    seed = 290797
    values = []

    for _ in range(4 * count):
        seed = seed * seed % 50515093
        values.append(seed % 500)

    return [tuple(values[index : index + 4]) for index in range(0, len(values), 4)]


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def trueIntersection(segment_one, segment_two):
    x1, y1, x2, y2 = segment_one
    x3, y3, x4, y4 = segment_two
    rx = x2 - x1
    ry = y2 - y1
    sx = x4 - x3
    sy = y4 - y3
    denominator = cross(rx, ry, sx, sy)

    if denominator == 0:
        return None

    qx = x3 - x1
    qy = y3 - y1
    t_numerator = cross(qx, qy, sx, sy)
    u_numerator = cross(qx, qy, rx, ry)

    if denominator < 0:
        denominator = -denominator
        t_numerator = -t_numerator
        u_numerator = -u_numerator

    if not (0 < t_numerator < denominator and 0 < u_numerator < denominator):
        return None

    x_numerator = x1 * denominator + t_numerator * rx
    y_numerator = y1 * denominator + t_numerator * ry
    x_divisor = math.gcd(abs(x_numerator), denominator)
    y_divisor = math.gcd(abs(y_numerator), denominator)

    return (
        x_numerator // x_divisor,
        denominator // x_divisor,
        y_numerator // y_divisor,
        denominator // y_divisor,
    )


def distinctIntersectionCount(segment_count):
    segments = generatedSegments(segment_count)
    intersections = set()

    for first in range(segment_count):
        for second in range(first + 1, segment_count):
            point = trueIntersection(segments[first], segments[second])
            if point is not None:
                intersections.add(point)

    return len(intersections)


def runTests():
    assert generatedSegments(1)[0] == (27, 144, 12, 232)
    assert trueIntersection((0, 0, 2, 2), (0, 2, 2, 0)) == (1, 1, 1, 1)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = distinctIntersectionCount(5000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
