import math
import time


def bezierDerivative(t, v):
    u = 1.0 - t
    dx = 3.0 * (2.0 * (v - 1.0) * u * t - v * t * t)
    dy = 3.0 * (v * u * u + 2.0 * (1.0 - v) * u * t)
    return dx, dy


def simpsonIntegral(function, intervals):
    step = 1.0 / intervals
    total = function(0.0) + function(1.0)

    for index in range(1, intervals):
        total += function(index * step) * (4 if index % 2 else 2)

    return total * step / 3.0


def bezierArea(v):
    return 0.5 + 0.6 * v - 0.15 * v * v


def circleAreaControl():
    # 1/2 + 3v/5 - 3v^2/20 = pi/4; take the smaller positive root.
    a = 0.15
    b = -0.6
    c = math.pi / 4.0 - 0.5
    return (-b - math.sqrt(b * b - 4.0 * a * c)) / (2.0 * a)


def bezierLength(v):
    return simpsonIntegral(lambda t: math.hypot(*bezierDerivative(t, v)), 200000)


def percentageDifference():
    v = circleAreaControl()
    length = bezierLength(v)
    quarterCircumference = math.pi / 2.0
    return 100.0 * (length - quarterCircumference) / quarterCircumference


def runTests():
    v = circleAreaControl()
    assert abs(bezierArea(v) - math.pi / 4.0) < 1e-14


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.10f}".format(percentageDifference())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
