import math
import time


def solveLinearSystem(matrix, values):
    size = len(values)
    rows = [row[:] + [value] for row, value in zip(matrix, values)]

    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(rows[row][column]))
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        for index in range(column, size + 1):
            rows[column][index] /= divisor

        for row in range(size):
            if row == column:
                continue
            scale = rows[row][column]
            for index in range(column, size + 1):
                rows[row][index] -= scale * rows[column][index]

    return [rows[row][size] for row in range(size)]


def expectedMatchLength(aWin, bWin, coinHeads):
    continueProbability = 1 - coinHeads
    draw = 1 - aWin - bWin
    constantReward = 1 / coinHeads

    middle = 1 - continueProbability * draw
    discriminant = math.sqrt(
        middle * middle
        - 4 * continueProbability * continueProbability * aWin * bWin
    )
    smallRoot = (middle - discriminant) / (2 * continueProbability * aWin)
    largeRoot = (middle + discriminant) / (2 * continueProbability * aWin)

    matrix = [
        [
            smallRoot * (1 - continueProbability * draw)
            - continueProbability * aWin * smallRoot * smallRoot,
            -continueProbability * bWin,
            0,
        ],
        [
            -continueProbability * aWin * smallRoot,
            1 - continueProbability * draw,
            -continueProbability * bWin,
        ],
        [
            0,
            -continueProbability * aWin,
            1 - continueProbability * draw
            - continueProbability * bWin / largeRoot,
        ],
    ]
    values = [
        aWin + draw
        - constantReward * (1 - continueProbability * aWin
                            - continueProbability * draw),
        aWin + continueProbability * aWin * constantReward,
        0,
    ]

    _, expectedFromTie, _ = solveLinearSystem(matrix, values)
    return expectedFromTie


def chessMatchSum(limit):
    total = 0
    for games in range(3, limit + 1):
        root = math.sqrt(games + 3)
        total += expectedMatchLength(
            1 / root,
            1 / root + 1 / (games * games),
            1 / (games ** 3),
        )
    return total


def runTests():
    assert round(expectedMatchLength(0.25, 0.25, 0.5), 6) == 0.585786
    assert round(expectedMatchLength(0.47, 0.48, 0.001), 6) == 377.471736
    assert round(chessMatchSum(3), 4) == 6.8345


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(chessMatchSum(50), ".4f")
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
