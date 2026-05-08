import time


def rowMasks(width):
    masks = []

    def build(position, mask):
        if position == width:
            masks.append(mask)
            return

        for brick in (2, 3):
            next_position = position + brick
            if next_position <= width:
                next_mask = mask
                if next_position < width:
                    next_mask |= 1 << next_position
                build(next_position, next_mask)

    build(0, 0)
    return masks


def crackFreeWalls(width, height):
    masks = rowMasks(width)
    compatible = {
        mask: [other for other in masks if mask & other == 0]
        for mask in masks
    }
    counts = {mask: 1 for mask in masks}

    for _ in range(1, height):
        counts = {
            mask: sum(counts[other] for other in compatible[mask])
            for mask in masks
        }

    return sum(counts.values())


def runTests():
    assert crackFreeWalls(9, 3) == 8


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = crackFreeWalls(32, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
