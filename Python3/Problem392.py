import math
import time


LIMIT = 400


def circleHeight(x):
    return math.sqrt(max(0.0, 1.0 - x * x))


def nextGridLine(previous, current):
    height = circleHeight(current)
    derivative = -current / height

    return current + (height - circleHeight(previous)) / derivative


def optimalPositiveGrid(lineCount):
    low = 0.0
    high = 1.0

    for _ in range(100):
        first = (low + high) / 2
        grid = [0.0, first]

        for index in range(1, lineCount + 1):
            if grid[index] >= 1.0:
                break

            grid.append(nextGridLine(grid[index - 1], grid[index]))

        endpoint = grid[lineCount + 1] if len(grid) > lineCount + 1 else 2.0

        if endpoint > 1.0:
            high = first
        else:
            low = first

    first = (low + high) / 2
    grid = [0.0, first]

    for index in range(1, lineCount + 1):
        grid.append(nextGridLine(grid[index - 1], grid[index]))

    grid[-1] = 1.0
    return grid


def enmeshedArea(innerLines=LIMIT):
    positiveLines = innerLines // 2
    grid = optimalPositiveGrid(positiveLines)
    quarterArea = sum(
        (grid[index + 1] - grid[index]) * circleHeight(grid[index])
        for index in range(positiveLines + 1)
    )

    return format(4 * quarterArea, ".10f")


def runTests():
    assert enmeshedArea(10) == "3.3469640797"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = enmeshedArea()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
