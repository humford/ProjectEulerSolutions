import time

import numpy as np


def move(distribution, degrees):
    contribution = distribution / degrees
    next_distribution = np.zeros_like(distribution)

    next_distribution[1:, :] += contribution[:-1, :]
    next_distribution[:-1, :] += contribution[1:, :]
    next_distribution[:, 1:] += contribution[:, :-1]
    next_distribution[:, :-1] += contribution[:, 1:]

    return next_distribution


def expectedEmptySquares(size, rings):
    degrees = np.full((size, size), 4.0)
    degrees[0, :] -= 1
    degrees[-1, :] -= 1
    degrees[:, 0] -= 1
    degrees[:, -1] -= 1

    empty_probabilities = np.ones((size, size))

    for start_row in range(size):
        for start_column in range(size):
            distribution = np.zeros((size, size))
            distribution[start_row, start_column] = 1.0

            for _ in range(rings):
                distribution = move(distribution, degrees)

            empty_probabilities *= 1 - distribution

    return empty_probabilities.sum()


def runTests():
    assert f"{expectedEmptySquares(2, 1):.6f}" == "1.000000"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f"{expectedEmptySquares(30, 50):.6f}"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
