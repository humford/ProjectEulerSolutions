from collections import defaultdict
import time


START = ".rbbrrbbrrbbrrbb"
TARGET = ".brbbrbrrbrbbrbr"
MODULUS = 100000007
CHECKSUM_BASE = 243
SIZE = 4

MOVES = (
    ("L", 76, 0, 1),
    ("R", 82, 0, -1),
    ("U", 85, 1, 0),
    ("D", 68, -1, 0),
)


def checksum(path):
    result = 0

    for move in path:
        result = (result * CHECKSUM_BASE + ord(move)) % MODULUS

    return result


def swapTiles(state, first, second):
    values = list(state)
    values[first], values[second] = values[second], values[first]
    return "".join(values)


def shortestChecksumSum(start, target):
    frontier = {start: [0]}
    visited = {start}

    while frontier:
        if target in frontier:
            return sum(frontier[target])

        next_frontier = defaultdict(list)

        for state, checksums in frontier.items():
            empty = state.index(".")
            row, col = divmod(empty, SIZE)

            for _, move_code, delta_row, delta_col in MOVES:
                next_row = row + delta_row
                next_col = col + delta_col

                if 0 <= next_row < SIZE and 0 <= next_col < SIZE:
                    next_empty = next_row * SIZE + next_col
                    next_state = swapTiles(state, empty, next_empty)

                    if next_state not in visited:
                        next_frontier[next_state].extend(
                            (value * CHECKSUM_BASE + move_code) % MODULUS
                            for value in checksums
                        )

        visited.update(next_frontier)
        frontier = next_frontier

    raise RuntimeError("target is unreachable")


def runTests():
    assert checksum("LULUR") == 19761398


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = shortestChecksumSum(START, TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
