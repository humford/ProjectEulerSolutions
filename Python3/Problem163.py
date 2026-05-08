import math
import time


def normalizedLine(point_one, point_two):
    x1, y1 = point_one
    x2, y2 = point_two
    a = y1 - y2
    b = x2 - x1
    c = a * x1 + b * y1
    divisor = math.gcd(math.gcd(abs(a), abs(b)), abs(c))

    if divisor:
        a //= divisor
        b //= divisor
        c //= divisor
    if a < 0 or (a == 0 and b < 0):
        a = -a
        b = -b
        c = -c

    return a, b, c


def crossHatchLines(size):
    lines = set()

    for i in range(size):
        lines.add(normalizedLine((0, 4 * i), (4, 4 * i)))

    for i in range(size):
        lines.add(normalizedLine((4 * i, 0), (3 + 4 * i, 2)))
        if i > 0:
            lines.add(normalizedLine((-4 * i, 0), (3 - 4 * i, 2)))

    for i in range(size):
        lines.add(normalizedLine((4 * i, 0), (2 + 4 * i, 4)))
        lines.add(normalizedLine((4 * i + 4, 0), (2 + 4 * i, 4)))

    for i in range(2 * size - 1):
        lines.add(normalizedLine((4 * i + 4, 0), (1 + 4 * i, 2)))

    for i in range(1, 2 * size):
        lines.add(normalizedLine((2 * i, 0), (2 * i, 4)))

    return sorted(lines)


def insideIntersection(line_one, line_two, size):
    a1, b1, c1 = line_one
    a2, b2, c2 = line_two
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None

    x = c1 * b2 - c2 * b1
    y = a1 * c2 - a2 * c1
    if determinant < 0:
        determinant = -determinant
        x = -x
        y = -y

    if y < 0 or y > 2 * x or y > 8 * size * determinant - 2 * x:
        return None

    return x, y, determinant


def samePoint(point_one, point_two):
    return (
        point_one[0] * point_two[2] == point_two[0] * point_one[2]
        and point_one[1] * point_two[2] == point_two[1] * point_one[2]
    )


def triangleCount(size):
    lines = crossHatchLines(size)
    intersections = [[None] * len(lines) for _ in lines]

    for first in range(len(lines)):
        for second in range(first + 1, len(lines)):
            intersections[first][second] = insideIntersection(lines[first], lines[second], size)

    count = 0
    for first in range(len(lines)):
        for second in range(first + 1, len(lines)):
            first_second = intersections[first][second]
            if first_second is None:
                continue

            for third in range(second + 1, len(lines)):
                first_third = intersections[first][third]
                second_third = intersections[second][third]
                if (
                    first_third is not None
                    and second_third is not None
                    and not (
                        samePoint(first_second, first_third)
                        and samePoint(first_second, second_third)
                    )
                ):
                    count += 1

    return count


def runTests():
    assert triangleCount(1) == 16
    assert triangleCount(2) == 104


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangleCount(36)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
