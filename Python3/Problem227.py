import time

import numpy as np


def expectedTurns(players):
    max_distance = players // 2
    matrix = np.eye(max_distance)
    constants = np.ones(max_distance)
    moves = {-1: 1 / 6, 0: 4 / 6, 1: 1 / 6}

    for distance in range(1, max_distance + 1):
        row = distance - 1
        for first_move, first_probability in moves.items():
            for second_move, second_probability in moves.items():
                raw_distance = (distance + second_move - first_move) % players
                next_distance = min(raw_distance, players - raw_distance)

                if next_distance > 0:
                    matrix[row, next_distance - 1] -= (
                        first_probability * second_probability
                    )

    expectations = np.linalg.solve(matrix, constants)
    return expectations[max_distance - 1]


def runTests():
    assert f"{expectedTurns(4):.10g}" == "7.2"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f"{expectedTurns(100):.10g}"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
