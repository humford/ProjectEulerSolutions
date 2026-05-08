import time
from pathlib import Path


def readMatrix():
    path = Path(__file__).resolve().parents[1] / "Files" / "p082_matrix.txt"
    return [
        [int(value) for value in line.split(",")]
        for line in path.read_text().strip().splitlines()
    ]


def minimalPathSum(matrix):
    row_count = len(matrix)
    col_count = len(matrix[0])
    costs = [matrix[row][0] for row in range(row_count)]

    for col in range(1, col_count):
        costs = [costs[row] + matrix[row][col] for row in range(row_count)]

        for row in range(1, row_count):
            costs[row] = min(costs[row], costs[row - 1] + matrix[row][col])

        for row in range(row_count - 2, -1, -1):
            costs[row] = min(costs[row], costs[row + 1] + matrix[row][col])

    return min(costs)


def runTests():
    example = [
        [131, 673, 234, 103, 18],
        [201, 96, 342, 965, 150],
        [630, 803, 746, 422, 111],
        [537, 699, 497, 121, 956],
        [805, 732, 524, 37, 331],
    ]
    assert minimalPathSum(example) == 994


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimalPathSum(readMatrix())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
