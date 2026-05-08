import time


def isExit(point):
    x, y = point
    return -0.01 <= x <= 0.01 and y > 0


def reflectedDirection(previous, current):
    incoming = (current[0] - previous[0], current[1] - previous[1])
    normal = (8 * current[0], 2 * current[1])
    dot = incoming[0] * normal[0] + incoming[1] * normal[1]
    normal_length_squared = normal[0] * normal[0] + normal[1] * normal[1]
    return (
        incoming[0] - 2 * dot * normal[0] / normal_length_squared,
        incoming[1] - 2 * dot * normal[1] / normal_length_squared,
    )


def nextIntersection(previous, current):
    dx, dy = reflectedDirection(previous, current)
    x, y = current

    a = 4 * dx * dx + dy * dy
    b = 8 * x * dx + 2 * y * dy
    t = -b / a

    return x + t * dx, y + t * dy


def reflectionCount():
    previous = (0.0, 10.1)
    current = (1.4, -9.6)
    hits = 1

    while True:
        following = nextIntersection(previous, current)
        if isExit(following):
            return hits
        previous, current = current, following
        hits += 1


def runTests():
    assert not isExit((1.4, -9.6))
    assert isExit((0.0, 10.0))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reflectionCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
