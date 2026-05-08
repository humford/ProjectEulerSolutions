import time


def isRightTriangle(point_one, point_two):
    x1, y1 = point_one
    x2, y2 = point_two

    return (
        x1 * x2 + y1 * y2 == 0
        or x1 * (x2 - x1) + y1 * (y2 - y1) == 0
        or x2 * (x1 - x2) + y2 * (y1 - y2) == 0
    )


def rightTriangleCount(limit):
    points = [
        (x, y)
        for x in range(limit + 1)
        for y in range(limit + 1)
        if x != 0 or y != 0
    ]
    count = 0

    for index, point_one in enumerate(points):
        for point_two in points[index + 1 :]:
            if isRightTriangle(point_one, point_two):
                count += 1

    return count


def runTests():
    assert rightTriangleCount(2) == 14


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rightTriangleCount(50)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
