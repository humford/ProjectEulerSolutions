import time


TARGET = 10**18
PERIOD_START = 9977
PERIOD = 104
PERIOD_BLACK_INCREMENT = 12


def blackSquareCounts(steps):
    black = set()
    x = 0
    y = 0
    direction = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    counts = []

    for _ in range(steps):
        position = (x, y)

        if position in black:
            black.remove(position)
            direction = (direction - 1) % 4
        else:
            black.add(position)
            direction = (direction + 1) % 4

        dx, dy = directions[direction]
        x += dx
        y += dy
        counts.append(len(black))

    return counts


def blackSquaresAfter(target=TARGET):
    simulatedSteps = PERIOD_START + PERIOD
    counts = blackSquareCounts(simulatedSteps)
    base = counts[PERIOD_START - 1]
    offset = target - PERIOD_START

    return (
        base
        + (offset // PERIOD) * PERIOD_BLACK_INCREMENT
        + counts[PERIOD_START - 1 + offset % PERIOD]
        - base
    )


def runTests():
    counts = blackSquareCounts(PERIOD_START + PERIOD)
    assert counts[PERIOD_START - 1] == 715
    assert counts[PERIOD_START - 1 + PERIOD] - counts[PERIOD_START - 1] == 12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = blackSquaresAfter()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
