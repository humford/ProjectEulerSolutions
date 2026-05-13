import time


N = 24


def quadtreeLength(exponent):
    size = 1 << exponent
    middle = size >> 1
    radius_squared = middle * middle

    def isBlack(x, y):
        dx = x - middle
        dy = y - middle
        return dx * dx + dy * dy <= radius_squared

    def encode(x0, y0, x1, y1, is_first=True):
        if x0 == x1:
            return 2

        bottom_left = isBlack(x0, y0)
        bottom_right = isBlack(x1, y0)
        top_right = isBlack(x1, y1)
        top_left = isBlack(x0, y1)

        if (
            not is_first
            and bottom_left == bottom_right == top_right == top_left
        ):
            return 2

        if x0 + 1 == x1:
            return 9

        half = (x1 - x0 + 1) // 2

        return (
            1
            + encode(x0, y0 + half, x1 - half, y1, False)
            + encode(x0 + half, y0 + half, x1, y1, False)
            + encode(x0, y0, x1 - half, y1 - half, False)
            + encode(x0 + half, y0, x1, y1 - half, False)
        )

    return encode(0, 0, size - 1, size - 1)


def runTests():
    assert quadtreeLength(1) == 9
    assert quadtreeLength(2) == 30
    assert quadtreeLength(8) == 4552


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = quadtreeLength(N)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
