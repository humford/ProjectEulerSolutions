import time
from pathlib import Path


def readMatrix():
    path = Path(__file__).resolve().parents[1] / "Files" / "p081_matrix.txt"
    return [
        [int(value) for value in line.split(",")]
        for line in path.read_text().strip().splitlines()
    ]


def minimalPathSum(matrix):
    totals = [row[:] for row in matrix]

    for row in range(len(totals)):
        for col in range(len(totals[row])):
            if row == 0 and col == 0:
                continue

            options = []
            if row > 0:
                options.append(totals[row - 1][col])
            if col > 0:
                options.append(totals[row][col - 1])

            totals[row][col] += min(options)

    return totals[-1][-1]


def runTests():
    example = [
        [131, 673, 234, 103, 18],
        [201, 96, 342, 965, 150],
        [630, 803, 746, 422, 111],
        [537, 699, 497, 121, 956],
        [805, 732, 524, 37, 331],
    ]
    assert minimalPathSum(example) == 2427


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimalPathSum(readMatrix())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
