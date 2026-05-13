import math
import time


def safeSqrt(value):
    if value < 0.0 and value > -1e-12:
        value = 0.0
    return math.sqrt(value)


def innerSoddyRadius(radiusA, radiusB, radiusC):
    curvatureA = 1.0 / radiusA
    curvatureB = 1.0 / radiusB
    curvatureC = 1.0 / radiusC
    curvature = (
        curvatureA
        + curvatureB
        + curvatureC
        + 2.0
        * math.sqrt(
            curvatureA * curvatureB
            + curvatureB * curvatureC
            + curvatureC * curvatureA
        )
    )
    return 1.0 / curvature


def thirdCircleCenter(radiusA, radiusB, radiusC):
    distanceAB = radiusA + radiusB
    distanceAC = radiusA + radiusC
    distanceBC = radiusB + radiusC
    x = (
        distanceAC * distanceAC
        - distanceBC * distanceBC
        + distanceAB * distanceAB
    ) / (2.0 * distanceAB)
    y = safeSqrt(distanceAC * distanceAC - x * x)
    return x, y


def tangencyPoints(radiusA, radiusB, radiusC, xC, yC):
    distanceAB = radiusA + radiusB
    distanceAC = radiusA + radiusC
    distanceBC = radiusB + radiusC

    pointAB = (float(radiusA), 0.0)
    pointAC = (radiusA * xC / distanceAC, radiusA * yC / distanceAC)
    pointBC = (
        distanceAB + radiusB * (xC - distanceAB) / distanceBC,
        radiusB * yC / distanceBC,
    )
    return pointAB, pointAC, pointBC


def circumcenter(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    determinant = 2.0 * (
        x1 * (y2 - y3)
        + x2 * (y3 - y1)
        + x3 * (y1 - y2)
    )
    if determinant == 0.0:
        raise ValueError("degenerate tangency triangle")

    square1 = x1 * x1 + y1 * y1
    square2 = x2 * x2 + y2 * y2
    square3 = x3 * x3 + y3 * y3
    x = (
        square1 * (y2 - y3)
        + square2 * (y3 - y1)
        + square3 * (y1 - y2)
    ) / determinant
    y = (
        square1 * (x3 - x2)
        + square2 * (x1 - x3)
        + square3 * (x2 - x1)
    ) / determinant
    return x, y


def incircleCenter(radiusA, radiusB, radiusC, xC, yC, innerRadius):
    distanceAB = radiusA + radiusB
    distanceEA = radiusA + innerRadius
    distanceEB = radiusB + innerRadius

    x = (
        distanceEA * distanceEA
        - distanceEB * distanceEB
        + distanceAB * distanceAB
    ) / (2.0 * distanceAB)
    y = safeSqrt(distanceEA * distanceEA - x * x)

    distanceEC = radiusC + innerRadius
    if abs(math.hypot(x - xC, y - yC) - distanceEC) < 1e-8:
        return x, y
    if abs(math.hypot(x - xC, -y - yC) - distanceEC) < 1e-8:
        return x, -y
    return x, y


def circularArcTriangleDistance(radiusA, radiusB, radiusC):
    xC, yC = thirdCircleCenter(radiusA, radiusB, radiusC)
    points = tangencyPoints(radiusA, radiusB, radiusC, xC, yC)
    xD, yD = circumcenter(*points)

    innerRadius = innerSoddyRadius(radiusA, radiusB, radiusC)
    xE, yE = incircleCenter(radiusA, radiusB, radiusC, xC, yC, innerRadius)
    return math.hypot(xD - xE, yD - yE)


def circularArcTriangleExpectation(limit=100):
    count = 0
    total = 0.0
    compensation = 0.0

    for radiusA in range(1, limit + 1):
        for radiusB in range(radiusA + 1, limit + 1):
            gcdAB = math.gcd(radiusA, radiusB)
            for radiusC in range(radiusB + 1, limit + 1):
                if math.gcd(gcdAB, radiusC) != 1:
                    continue

                count += 1
                value = circularArcTriangleDistance(radiusA, radiusB, radiusC)
                adjusted = value - compensation
                nextTotal = total + adjusted
                compensation = (nextTotal - total) - adjusted
                total = nextTotal

    return total / count


def runTests():
    radiusA, radiusB, radiusC = 1, 2, 3
    xC, yC = thirdCircleCenter(radiusA, radiusB, radiusC)
    points = tangencyPoints(radiusA, radiusB, radiusC, xC, yC)
    xD, yD = circumcenter(*points)
    distances = [math.hypot(xD - x, yD - y) for x, y in points]
    assert max(distances) - min(distances) < 1e-10

    innerRadius = innerSoddyRadius(radiusA, radiusB, radiusC)
    xE, yE = incircleCenter(radiusA, radiusB, radiusC, xC, yC, innerRadius)
    assert abs(math.hypot(xE, yE) - (radiusA + innerRadius)) < 1e-8
    assert abs(math.hypot(xE - (radiusA + radiusB), yE) - (radiusB + innerRadius)) < 1e-8
    assert abs(math.hypot(xE - xC, yE - yC) - (radiusC + innerRadius)) < 1e-8


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(circularArcTriangleExpectation(), ".8f")
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
