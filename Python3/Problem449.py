import math
import time


def spheroidSurfaceArea(a, b):
    if a == b:
        return 4 * math.pi * a * a

    if a > b:
        eccentricity = math.sqrt(1 - b * b / (a * a))
        return 2 * math.pi * a * a * (
            1
            + (1 - eccentricity * eccentricity)
            / eccentricity
            * math.atanh(eccentricity)
        )

    eccentricity = math.sqrt(1 - a * a / (b * b))
    return 2 * math.pi * a * a * (1 + b / (a * eccentricity) * math.asin(eccentricity))


def integratedMeanCurvature(a, b):
    if a == b:
        return 4 * math.pi * a

    if a > b:
        focus = math.sqrt(a * a - b * b)
        integral = 2 / (b * focus) * math.atan(focus / b)
    else:
        focus = math.sqrt(b * b - a * a)
        integral = 2 / (b * focus) * math.atanh(focus / b)

    return math.pi * b * (2 + a * a * integral)


def chocolateVolume(a, b):
    return (
        spheroidSurfaceArea(a, b)
        + integratedMeanCurvature(a, b)
        + 4 * math.pi / 3
    )


def answer():
    return format(chocolateVolume(3, 1), ".8f")


def runTests():
    assert format(chocolateVolume(1, 1), ".8f") == format(28 * math.pi / 3, ".8f")
    assert format(chocolateVolume(2, 1), ".8f") == "60.35475635"


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
