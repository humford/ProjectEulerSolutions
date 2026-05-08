import functools
import time


def triominoTilings(width, height):
    if width > height:
        width, height = height, width

    size = width * height

    @functools.lru_cache(maxsize=None)
    def count(position, mask):
        while mask & 1:
            position += 1
            mask >>= 1

        if position == size:
            return 1 if mask == 0 else 0

        col = position % width
        shapes = []

        if col + 2 < width:
            shapes.append((0, 1, 2))
        if position + 2 * width < size:
            shapes.append((0, width, 2 * width))
        if col + 1 < width and position + width + 1 < size:
            shapes.extend(
                [
                    (0, 1, width),
                    (0, 1, width + 1),
                    (0, width, width + 1),
                ]
            )
        if col > 0 and position + width < size:
            shapes.append((0, width - 1, width))

        total = 0
        for shape in shapes:
            bits = sum(1 << offset for offset in shape)
            if mask & bits == 0:
                total += count(position + 1, (mask | bits) >> 1)

        return total

    return count(0, 0)


def runTests():
    assert triominoTilings(2, 9) == 41


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triominoTilings(9, 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
