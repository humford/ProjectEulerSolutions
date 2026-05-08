import math
import time


def descartesCurvature(a, b, c):
    return a + b + c + 2 * math.sqrt(a * b + a * c + b * c)


def filledArea(depth, a, b, c):
    if depth == 0:
        return 0

    new_curvature = descartesCurvature(a, b, c)
    return (
        1 / (new_curvature * new_curvature)
        + filledArea(depth - 1, new_curvature, a, b)
        + filledArea(depth - 1, new_curvature, a, c)
        + filledArea(depth - 1, new_curvature, b, c)
    )


def uncoveredFraction(iterations):
    inner = 1
    outer = 3 - 2 * math.sqrt(3)
    outer_area = 1 / (outer * outer)
    covered_area = 3 / (inner * inner)

    covered_area += filledArea(iterations, inner, inner, inner)
    covered_area += 3 * filledArea(iterations, outer, inner, inner)

    return 1 - covered_area / outer_area


def runTests():
    assert f"{uncoveredFraction(10):.8f}" == "0.00396087"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f"{uncoveredFraction(10):.8f}"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
