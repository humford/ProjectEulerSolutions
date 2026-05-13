import math
import time


SMALL_CIRCLE_RADIUS = 0.999


def nanobotLength(bots):
    k = math.sin(math.pi / bots)
    a = math.sqrt(1 - k * k)
    r = SMALL_CIRCLE_RADIUS
    q = math.sqrt(1 - k * k * r * r)

    integral = (
        a * math.asinh(a * r / math.sqrt(1 - r * r))
        + k * math.atan(k * r / q)
    )
    return integral / k


def roundedLength(length):
    return f"{length:.2f}"


def totalNanobotLength(bots):
    return roundedLength(bots * nanobotLength(bots))


def targetBotCount(minimumLength):
    bots = 3
    while nanobotLength(bots) <= minimumLength:
        bots += 1
    return bots


def targetNanobotLength():
    bots = targetBotCount(1000)
    return totalNanobotLength(bots)


def runTests():
    assert roundedLength(nanobotLength(3)) == "2.84"
    assert totalNanobotLength(3) == "8.52"
    assert nanobotLength(targetBotCount(1000) - 1) <= 1000
    assert nanobotLength(targetBotCount(1000)) > 1000


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = targetNanobotLength()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
