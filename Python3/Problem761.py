import math
import time


def branchIndex(sides):
    theta = math.pi / sides
    tangent = math.tan(theta)

    index = 0
    while True:
        value = math.sin(index * theta) - (index + sides) * tangent * math.cos(index * theta)
        if value >= 0:
            return index - 1
        index += 1


def criticalSpeedRegularPolygon(sides):
    theta = math.pi / sides
    index = branchIndex(sides)
    argument = (
        2 * math.sin(index * theta) / ((index + sides) * math.tan(theta))
        - math.cos(index * theta)
    )
    argument = max(-1.0, min(1.0, argument))
    alpha = (index * theta + math.acos(argument)) / 2
    return 1 / math.cos(alpha)


def circularCriticalSpeed():
    low = 0.0
    high = math.pi / 2

    for _ in range(200):
        mid = (low + high) / 2
        value = mid + math.pi - math.tan(mid)
        if value > 0:
            low = mid
        else:
            high = mid

    return 1 / math.cos((low + high) / 2)


def runTests():
    assert format(circularCriticalSpeed(), ".8f") == "4.60333885"
    assert branchIndex(4) == 1
    assert format(criticalSpeedRegularPolygon(4), ".8f") == "5.78859314"
    assert branchIndex(6) == 2


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = criticalSpeedRegularPolygon(6)
    elapsed = time.time() - start

    print("Found " + format(answer, ".8f") + " in " + str(elapsed) + " seconds.")
