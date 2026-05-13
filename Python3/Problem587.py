import time
from math import asin, pi, sqrt


L_SECTION_AREA = 1 - pi / 4


def circleIntersectionX(circleCount):
    n = circleCount
    return n * (n + 1 - sqrt(2 * n)) / (n * n + 1)


def concaveTriangleArea(circleCount):
    intersectionX = circleIntersectionX(circleCount)
    shiftedX = intersectionX - 1
    arcIntegral = 0.5 * (
        shiftedX * sqrt(1 - shiftedX * shiftedX) + asin(shiftedX)
    )

    triangleArea = intersectionX * intersectionX / (2 * circleCount)
    circularSegmentArea = 1 - intersectionX + arcIntegral
    return triangleArea + circularSegmentArea


def concaveTriangleRatio(circleCount):
    return concaveTriangleArea(circleCount) / L_SECTION_AREA


def leastCircleCount(threshold):
    low = 1
    high = 2
    while concaveTriangleRatio(high) >= threshold:
        high *= 2

    while low + 1 < high:
        mid = (low + high) // 2
        if concaveTriangleRatio(mid) < threshold:
            high = mid
        else:
            low = mid

    return high


def runTests():
    assert abs(concaveTriangleRatio(1) - 0.5) < 1e-12
    assert abs(concaveTriangleRatio(2) - 0.364626) < 1e-6
    assert leastCircleCount(0.10) == 15
    assert concaveTriangleRatio(14) >= 0.10
    assert concaveTriangleRatio(15) < 0.10


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastCircleCount(0.001)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
