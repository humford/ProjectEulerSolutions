import math
import time


def triangularWaveIntegral(frac):
    if frac <= 0.5:
        return frac * frac / 2
    return frac - frac * frac / 2 - 0.25


def periodicTriangularIntegral(value):
    whole = math.floor(value)
    return whole / 4 + triangularWaveIntegral(value - whole)


def blancmange(x, terms=80):
    total = 0.0
    scale = 1.0

    for _ in range(terms):
        total += abs(scale * x - round(scale * x)) / scale
        scale *= 2

    return total


def blancmangeIntegral(a, b, terms=80):
    total = 0.0
    scale = 1.0

    for _ in range(terms):
        total += (
            periodicTriangularIntegral(scale * b)
            - periodicTriangularIntegral(scale * a)
        ) / (scale * scale)
        scale *= 2

    return total


def circleLower(x):
    return 0.5 - math.sqrt(1 / 16 - (x - 0.25) ** 2)


def circleLowerIntegral(a, b):
    radius = 0.25
    center_x = 0.25

    def antiderivative(x):
        u = x - center_x
        circle_piece = 0.5 * u * math.sqrt(max(0.0, radius * radius - u * u))
        circle_piece += 0.5 * radius * radius * math.asin(u / radius)
        return 0.5 * x - circle_piece

    return antiderivative(b) - antiderivative(a)


def intersection():
    low = 0.0
    high = 0.25

    for _ in range(100):
        midpoint = (low + high) / 2
        if blancmange(midpoint) > circleLower(midpoint):
            high = midpoint
        else:
            low = midpoint

    return (low + high) / 2


def enclosedArea():
    start = intersection()
    return blancmangeIntegral(start, 0.5) - circleLowerIntegral(start, 0.5)


def runTests():
    assert f"{enclosedArea():.8f}" == "0.11316017"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f"{enclosedArea():.8f}"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
