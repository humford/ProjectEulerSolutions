import math
import time


TOTAL_EAST_DISTANCE = 100
MARSH_WIDTH = 50
MARSH_STRIP_WIDTH = 10
NORMAL_DISTANCE = TOTAL_EAST_DISTANCE / math.sqrt(2)
TANGENT_DISTANCE = TOTAL_EAST_DISTANCE / math.sqrt(2)
OUTSIDE_WIDTH = (NORMAL_DISTANCE - MARSH_WIDTH) / 2

STRIP_WIDTHS = [
    OUTSIDE_WIDTH,
    MARSH_STRIP_WIDTH,
    MARSH_STRIP_WIDTH,
    MARSH_STRIP_WIDTH,
    MARSH_STRIP_WIDTH,
    MARSH_STRIP_WIDTH,
    OUTSIDE_WIDTH,
]
SPEEDS = [10, 9, 8, 7, 6, 5, 10]


def travelTimeForTangentDistances(tangentDistances):
    return sum(
        math.hypot(width, tangent) / speed
        for width, tangent, speed in zip(STRIP_WIDTHS, tangentDistances, SPEEDS)
    )


def straightCrossingTime():
    return travelTimeForTangentDistances(STRIP_WIDTHS)


def tangentDistanceSum(snellConstant):
    total = 0
    for width, speed in zip(STRIP_WIDTHS, SPEEDS):
        scaled = snellConstant * speed
        total += width * scaled / math.sqrt(1 - scaled * scaled)
    return total


def optimalTangentDistances():
    low = 0
    high = 1 / max(SPEEDS)
    for _ in range(100):
        mid = (low + high) / 2
        if tangentDistanceSum(mid) < TANGENT_DISTANCE:
            low = mid
        else:
            high = mid

    snellConstant = (low + high) / 2
    return [
        width * snellConstant * speed
        / math.sqrt(1 - (snellConstant * speed) ** 2)
        for width, speed in zip(STRIP_WIDTHS, SPEEDS)
    ]


def optimalCrossingTime():
    return travelTimeForTangentDistances(optimalTangentDistances())


def marshCrossingTime(kind):
    if kind == "straight":
        return f"{straightCrossingTime():.4f}"
    if kind == "optimal":
        return f"{optimalCrossingTime():.10f}"
    raise ValueError("unknown crossing kind")


def runTests():
    assert marshCrossingTime("straight") == "13.4738"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = marshCrossingTime("optimal")
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
