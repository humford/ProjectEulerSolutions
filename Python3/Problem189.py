import functools
import time


COLORS = (0, 1, 2)


@functools.cache
def compatibleRows(restrictions):
    row_length = len(restrictions)
    rows = []

    def build(position, row):
        if position == row_length:
            rows.append(tuple(row))
            return

        for color in COLORS:
            if color == restrictions[position]:
                continue
            if position > 0 and color == row[-1]:
                continue

            row.append(color)
            build(position + 1, row)
            row.pop()

    build(0, [])
    return tuple(rows)


def nextRowRestrictions(upper_row):
    restrictions = [-1] * (len(upper_row) + 2)
    for position in range(0, len(upper_row), 2):
        restrictions[position + 1] = upper_row[position]

    return tuple(restrictions)


def triangularGridColorings(size):
    counts = {(color,): 1 for color in COLORS}

    for _ in range(1, size):
        next_counts = {}
        for upper_row, count in counts.items():
            restrictions = nextRowRestrictions(upper_row)
            for lower_row in compatibleRows(restrictions):
                next_counts[lower_row] = next_counts.get(lower_row, 0) + count
        counts = next_counts

    return sum(counts.values())


def runTests():
    assert triangularGridColorings(1) == 3
    assert triangularGridColorings(2) == 24


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangularGridColorings(8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
