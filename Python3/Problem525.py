import math
import time


INTEGRATION_STEPS = 512


def centerPathIntegrand(a, b, angle):
    sine = math.sin(angle)
    cosine = math.cos(angle)
    sineSquared = sine * sine
    cosineSquared = cosine * cosine

    centerToContact = math.sqrt(a * a * cosineSquared + b * b * sineSquared)
    tangentAngleDerivative = (
        a * b / (a * a * sineSquared + b * b * cosineSquared)
    )
    return centerToContact * tangentAngleDerivative


def simpsonIntegral(function, start, end, intervals):
    if intervals % 2:
        intervals += 1

    step = (end - start) / intervals
    total = function(start) + function(end)

    for index in range(1, intervals):
        coefficient = 4 if index % 2 else 2
        total += coefficient * function(start + index * step)

    return total * step / 3


def rollingEllipseLength(a, b):
    # One quadrant determines the full turn by symmetry.
    quarterLength = simpsonIntegral(
        lambda angle: centerPathIntegrand(a, b, angle),
        0,
        math.pi / 2,
        INTEGRATION_STEPS,
    )
    return 4 * quarterLength


def roundedLength(value):
    return f"{value:.8f}"


def targetLengthSum():
    return roundedLength(rollingEllipseLength(1, 4) + rollingEllipseLength(3, 4))


def runTests():
    assert roundedLength(rollingEllipseLength(2, 4)) == "21.38816906"
    assert roundedLength(rollingEllipseLength(3, 3)) == roundedLength(6 * math.pi)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = targetLengthSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
