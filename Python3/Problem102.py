import time
from pathlib import Path


def readTriangles():
    path = Path(__file__).resolve().parents[1] / "Files" / "p102_triangles.txt"
    triangles = []

    for line in path.read_text().strip().splitlines():
        values = [int(value) for value in line.split(",")]
        triangles.append([(values[index], values[index + 1]) for index in range(0, 6, 2)])

    return triangles


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def containsOrigin(triangle):
    signs = []

    for index, point in enumerate(triangle):
        next_point = triangle[(index + 1) % 3]
        value = cross(point, next_point)
        signs.append(value)

    return all(value > 0 for value in signs) or all(value < 0 for value in signs)


def originContainingTriangleCount(triangles):
    return sum(containsOrigin(triangle) for triangle in triangles)


def runTests():
    assert containsOrigin([(-340, 495), (-153, -910), (835, -947)])
    assert not containsOrigin([(-175, 41), (-421, -714), (574, -645)])


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = originContainingTriangleCount(readTriangles())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
