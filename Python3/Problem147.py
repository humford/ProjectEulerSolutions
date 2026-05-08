import time


def axisAlignedRectangles(width, height):
    return width * (width + 1) * height * (height + 1) // 4


def diagonalRectangles(width, height):
    total = 0
    u_values = range(width + height + 1)

    for first_index, first_u in enumerate(u_values):
        for second_u in range(first_u + 1, width + height + 1):
            low = max(
                -first_u,
                -second_u,
                first_u - 2 * height,
                second_u - 2 * height,
            )
            high = min(
                2 * width - first_u,
                2 * width - second_u,
                first_u,
                second_u,
            )
            choices = high - low + 1
            if choices >= 2:
                total += choices * (choices - 1) // 2

    return total


def rectangles(width, height):
    return axisAlignedRectangles(width, height) + diagonalRectangles(width, height)


def rectanglesInGrids(max_width, max_height):
    return sum(
        rectangles(width, height)
        for width in range(1, max_width + 1)
        for height in range(1, max_height + 1)
    )


def runTests():
    assert rectangles(3, 2) == 37
    assert rectanglesInGrids(3, 2) == 72


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rectanglesInGrids(47, 43)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
