from math import ceil, cos, floor, pi, radians, sin, sqrt, tan
import time


SIMPSON_STEPS = 2048


def distanceIntegral(offset, radius, steps=SIMPSON_STEPS):
    step = pi / steps
    total = 0.0

    for index in range(steps + 1):
        angle = index * step
        sine = sin(angle)
        distanceToWall = (
            -offset * cos(angle)
            + sqrt(radius * radius - offset * offset * sine * sine)
        )
        value = distanceToWall * distanceToWall * distanceToWall

        if index == 0 or index == steps:
            weight = 1
        elif index % 2:
            weight = 4
        else:
            weight = 2

        total += weight * value

    return 2 * step * total / 9


def wastedVolume(offset, radius, angleDegrees):
    return tan(radians(angleDegrees)) * distanceIntegral(offset, radius)


def rootForWastedVolume(target, radius, angleDegrees):
    lower = 0.0
    upper = radius

    for _ in range(80):
        middle = (lower + upper) / 2
        if wastedVolume(middle, radius, angleDegrees) < target:
            lower = middle
        else:
            upper = middle

    return (lower + upper) / 2


def squareWastageSolutions(radius, angleDegrees):
    minimumSquare = ceil(sqrt(wastedVolume(0.0, radius, angleDegrees)))
    maximumSquare = floor(sqrt(wastedVolume(radius, radius, angleDegrees)))
    return [
        rootForWastedVolume(square * square, radius, angleDegrees)
        for square in range(minimumSquare, maximumSquare + 1)
    ]


def siloSolutionSum():
    return format(sum(squareWastageSolutions(6, 40)), ".9f")


def runTests():
    assert format(wastedVolume(0.0, 3, 30), ".9f") == "32.648388556"

    diameterSixSolutions = squareWastageSolutions(3, 30)
    assert len(diameterSixSolutions) == 2
    assert format(diameterSixSolutions[0], ".9f") == "1.114785284"
    assert format(diameterSixSolutions[1], ".9f") == "2.511167869"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = siloSolutionSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
