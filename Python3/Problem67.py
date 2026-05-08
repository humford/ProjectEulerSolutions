import time
from pathlib import Path


def readTriangle():
    path = Path(__file__).resolve().parents[1] / "Files" / "p067_triangle.txt"
    return [
        [int(value) for value in line.split()]
        for line in path.read_text().strip().splitlines()
    ]


def maximumPathSum(triangle):
    totals = triangle[-1][:]

    for row in reversed(triangle[:-1]):
        totals = [
            value + max(totals[index], totals[index + 1])
            for index, value in enumerate(row)
        ]

    return totals[0]


def runTests():
    assert maximumPathSum([[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]) == 23


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumPathSum(readTriangle())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
