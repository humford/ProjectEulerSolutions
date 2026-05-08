import heapq
import time
from pathlib import Path


def readMatrix():
    path = Path(__file__).resolve().parents[1] / "Files" / "p083_matrix.txt"
    return [
        [int(value) for value in line.split(",")]
        for line in path.read_text().strip().splitlines()
    ]


def minimalPathSum(matrix):
    row_count = len(matrix)
    col_count = len(matrix[0])
    target = (row_count - 1, col_count - 1)
    distances = {(0, 0): matrix[0][0]}
    queue = [(matrix[0][0], 0, 0)]

    while queue:
        distance, row, col = heapq.heappop(queue)
        if distance != distances[(row, col)]:
            continue
        if (row, col) == target:
            return distance

        for next_row, next_col in (
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ):
            if not (0 <= next_row < row_count and 0 <= next_col < col_count):
                continue

            next_distance = distance + matrix[next_row][next_col]
            if next_distance < distances.get((next_row, next_col), float("inf")):
                distances[(next_row, next_col)] = next_distance
                heapq.heappush(queue, (next_distance, next_row, next_col))

    raise ValueError("No path found")


def runTests():
    example = [
        [131, 673, 234, 103, 18],
        [201, 96, 342, 965, 150],
        [630, 803, 746, 422, 111],
        [537, 699, 497, 121, 956],
        [805, 732, 524, 37, 331],
    ]
    assert minimalPathSum(example) == 2297


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimalPathSum(readMatrix())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
