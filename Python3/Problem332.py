import math
import time


LIMIT = 50


def spherePoints(radius):
    points = []
    radiusSquare = radius * radius

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            zSquare = radiusSquare - x * x - y * y

            if zSquare < 0:
                continue

            z = math.isqrt(zSquare)

            if z * z == zSquare:
                points.append((x, y, z))

                if z != 0:
                    points.append((x, y, -z))

    return points


def smallestSphericalTriangleArea(radius):
    points = spherePoints(radius)
    pointCount = len(points)
    radiusSquare = radius * radius
    radiusCubed = radius * radiusSquare
    best = float("inf")

    for i in range(pointCount - 2):
        ax, ay, az = points[i]

        for j in range(i + 1, pointCount - 1):
            bx, by, bz = points[j]
            crossX = ay * bz - az * by
            crossY = az * bx - ax * bz
            crossZ = ax * by - ay * bx
            dotAB = ax * bx + ay * by + az * bz

            for k in range(j + 1, pointCount):
                cx, cy, cz = points[k]
                determinant = crossX * cx + crossY * cy + crossZ * cz

                if determinant == 0:
                    continue

                if determinant < 0:
                    determinant = -determinant

                denominator = radiusCubed + radius * (
                    dotAB
                    + ax * cx
                    + ay * cy
                    + az * cz
                    + bx * cx
                    + by * cy
                    + bz * cz
                )
                area = radiusSquare * 2.0 * math.atan2(determinant, denominator)

                if area < best:
                    best = area

    return best


def sphericalTriangleAreaSum(limit=LIMIT):
    return sum(smallestSphericalTriangleArea(radius) for radius in range(1, limit + 1))


def runTests():
    assert round(smallestSphericalTriangleArea(14), 6) == 3.294040


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.6f}".format(sphericalTriangleAreaSum())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
