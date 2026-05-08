import time
from collections import defaultdict


CELL_SIZE = 512


def laggedFibonacciValues(count):
    values = [0] * (count + 1)

    for k in range(1, min(count, 55) + 1):
        values[k] = (100003 - 200003 * k + 300007 * k * k * k) % 1000000

    for k in range(56, count + 1):
        values[k] = (values[k - 24] + values[k - 55]) % 1000000

    return values


def cuboids(count):
    values = laggedFibonacciValues(6 * count)
    boxes = []

    for n in range(1, count + 1):
        index = 6 * n
        x = values[index - 5] % 10000
        y = values[index - 4] % 10000
        z = values[index - 3] % 10000
        dx = 1 + values[index - 2] % 399
        dy = 1 + values[index - 1] % 399
        dz = 1 + values[index] % 399
        boxes.append((x, x + dx, y, y + dy, z, z + dz))

    return boxes


def volume(box):
    return (box[1] - box[0]) * (box[3] - box[2]) * (box[5] - box[4])


def intersection(first, second):
    x1 = max(first[0], second[0])
    x2 = min(first[1], second[1])
    if x1 >= x2:
        return None

    y1 = max(first[2], second[2])
    y2 = min(first[3], second[3])
    if y1 >= y2:
        return None

    z1 = max(first[4], second[4])
    z2 = min(first[5], second[5])
    if z1 >= z2:
        return None

    return (x1, x2, y1, y2, z1, z2)


def coveredCells(box):
    for x_cell in range(box[0] // CELL_SIZE, (box[1] - 1) // CELL_SIZE + 1):
        for y_cell in range(box[2] // CELL_SIZE, (box[3] - 1) // CELL_SIZE + 1):
            for z_cell in range(box[4] // CELL_SIZE, (box[5] - 1) // CELL_SIZE + 1):
                yield (x_cell, y_cell, z_cell)


def combinedVolume(boxes):
    signed_boxes = []
    buckets = defaultdict(list)
    total = 0

    for box in boxes:
        candidates = set()
        for cell in coveredCells(box):
            candidates.update(buckets.get(cell, ()))

        additions = [(1, box)]
        for signed_index in candidates:
            sign, existing_box = signed_boxes[signed_index]
            overlap = intersection(box, existing_box)
            if overlap is not None:
                additions.append((-sign, overlap))

        for sign, addition in additions:
            signed_index = len(signed_boxes)
            signed_boxes.append((sign, addition))
            total += sign * volume(addition)
            for cell in coveredCells(addition):
                buckets[cell].append(signed_index)

    return total


def runTests():
    assert cuboids(2) == [
        (7, 101, 53, 422, 183, 239),
        (2383, 2425, 3563, 3775, 5079, 5423),
    ]
    assert combinedVolume(cuboids(100)) == 723581599


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = combinedVolume(cuboids(50000))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
