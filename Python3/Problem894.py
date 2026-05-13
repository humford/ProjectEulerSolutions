import math
import time


def clamped(value, low, high):
    return max(low, min(high, value))


def normalizedTangencyDistance(scale, theta, index):
    power = scale**index
    numerator = 1 + power * power - 2 * power * math.cos(index * theta)
    denominator = (1 + power) ** 2
    return numerator / denominator


def residuals(scale, theta):
    base = normalizedTangencyDistance(scale, theta, 1)
    return (
        base - normalizedTangencyDistance(scale, theta, 7),
        base - normalizedTangencyDistance(scale, theta, 8),
    )


def residualNorm(scale, theta):
    first, second = residuals(scale, theta)
    return first * first + second * second


def initialGuess():
    bestScale = 0.9
    bestTheta = 0.8
    bestNorm = float("inf")

    scale = 0.75
    while scale <= 0.99:
        theta = 0.05
        while theta <= math.pi - 0.05:
            value = residualNorm(scale, theta)
            if value < bestNorm:
                bestScale = scale
                bestTheta = theta
                bestNorm = value
            theta += 0.01
        scale += 0.002

    return bestScale, bestTheta


def solveTangencyParameters():
    scale, theta = initialGuess()

    for _ in range(60):
        first, second = residuals(scale, theta)
        if max(abs(first), abs(second)) < 1e-15:
            break

        deltaScale = 1e-8
        deltaTheta = 1e-8

        firstPlusScale, secondPlusScale = residuals(scale + deltaScale, theta)
        firstMinusScale, secondMinusScale = residuals(scale - deltaScale, theta)
        firstPlusTheta, secondPlusTheta = residuals(scale, theta + deltaTheta)
        firstMinusTheta, secondMinusTheta = residuals(scale, theta - deltaTheta)

        a = (firstPlusScale - firstMinusScale) / (2 * deltaScale)
        b = (firstPlusTheta - firstMinusTheta) / (2 * deltaTheta)
        c = (secondPlusScale - secondMinusScale) / (2 * deltaScale)
        d = (secondPlusTheta - secondMinusTheta) / (2 * deltaTheta)

        determinant = a * d - b * c
        if determinant == 0 or not math.isfinite(determinant):
            break

        stepScale = (d * first - b * second) / determinant
        stepTheta = (-c * first + a * second) / determinant
        currentNorm = residualNorm(scale, theta)
        step = 1.0

        while step > 2**-40:
            nextScale = scale - step * stepScale
            nextTheta = theta - step * stepTheta
            if not (0 < nextScale < 1 and 0 < nextTheta < math.pi):
                step *= 0.5
                continue

            nextNorm = residualNorm(nextScale, nextTheta)
            if nextNorm < currentNorm:
                scale = nextScale
                theta = nextTheta
                break

            step *= 0.5

    first, second = residuals(scale, theta)
    assert abs(first) < 1e-12
    assert abs(second) < 1e-12
    return scale, theta


def curvilinearTriangleArea(r1, r2, r3):
    side1 = r2 + r3
    side2 = r1 + r3
    side3 = r1 + r2

    semiperimeter = (side1 + side2 + side3) / 2
    triangleArea = math.sqrt(
        max(
            0.0,
            semiperimeter
            * (semiperimeter - side1)
            * (semiperimeter - side2)
            * (semiperimeter - side3),
        )
    )

    angle1 = math.acos(
        clamped(
            (side2 * side2 + side3 * side3 - side1 * side1)
            / (2 * side2 * side3),
            -1,
            1,
        )
    )
    angle2 = math.acos(
        clamped(
            (side1 * side1 + side3 * side3 - side2 * side2)
            / (2 * side1 * side3),
            -1,
            1,
        )
    )
    angle3 = math.acos(
        clamped(
            (side1 * side1 + side2 * side2 - side3 * side3)
            / (2 * side1 * side2),
            -1,
            1,
        )
    )

    sectors = (
        r1 * r1 * angle1
        + r2 * r2 * angle2
        + r3 * r3 * angle3
    ) / 2
    return triangleArea - sectors


def totalArea():
    scale, theta = solveTangencyParameters()
    radius7 = scale**7
    radius8 = radius7 * scale

    areaA = curvilinearTriangleArea(1, scale, radius8)
    areaB = curvilinearTriangleArea(1, radius7, radius8)
    return (areaA + areaB) / (1 - scale * scale)


def solve():
    return f"{totalArea():.10f}"


def runTests():
    scale, theta = solveTangencyParameters()
    first, second = residuals(scale, theta)
    assert abs(first) < 1e-12
    assert abs(second) < 1e-12
    assert curvilinearTriangleArea(1, 1, 1) > 0
    assert solve() == "0.7718678168"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
