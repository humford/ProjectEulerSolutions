import math
import time


TUBE_RADIUS = 50


def centerDistance(first_radius, second_radius):
    return 2 * math.sqrt(
        TUBE_RADIUS * (first_radius + second_radius - TUBE_RADIUS)
    )


def minimumLength(radii):
    ordering = list(range(max(radii), min(radii) - 1, -2)) + list(
        range(min(radii) + 1, max(radii), 2)
    )
    length = ordering[0] + ordering[-1]

    for first, second in zip(ordering, ordering[1:]):
        length += centerDistance(first, second)

    return length


def runTests():
    assert round((30 + 50 + centerDistance(30, 50)) * 1000) == 157460


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = round(minimumLength(range(30, 51)) * 1000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
