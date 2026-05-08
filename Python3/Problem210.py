import math
import time


def circleContribution(radius):
    s = radius // 8
    circle_radius_squared = 2 * s * s
    total = 0
    y = math.isqrt(circle_radius_squared) + 1
    x = 0

    while x * x <= circle_radius_squared:
        while y >= 0 and x * x + y * y >= circle_radius_squared:
            y -= 1

        if x == 0:
            total += 2 * y
        elif y >= 0:
            total += 4 * y + 2

        x += 1

    return total - 2 * (s - 1)


def obtuseTrianglePointCount(radius):
    return 3 * radius * radius // 2 + circleContribution(radius)


def runTests():
    assert obtuseTrianglePointCount(8) == 100


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = obtuseTrianglePointCount(1000000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
