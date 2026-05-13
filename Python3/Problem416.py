import math
import time

import numpy as np


MODULUS = 10**9
TARGET_M = 10
TARGET_N = 10**12


def stateIndex(pathCount):
    states = []
    index = {}

    for missed in range(2):
        for dueNow in range(pathCount + 1):
            for dueNext in range(pathCount - dueNow + 1):
                dueLater = pathCount - dueNow - dueNext
                state = (dueNow, dueNext, dueLater, missed)
                index[state] = len(states)
                states.append(state)

    return states, index


def transitionMatrix(pathCount, modulus):
    states, index = stateIndex(pathCount)
    matrix = np.zeros((len(states), len(states)), dtype=np.int64)
    factorials = [math.factorial(value) for value in range(pathCount + 1)]

    for stateNumber, (dueNow, dueNext, dueLater, missed) in enumerate(states):
        for jumpOne in range(dueNow + 1):
            for jumpTwo in range(dueNow - jumpOne + 1):
                jumpThree = dueNow - jumpOne - jumpTwo
                nextDueNow = jumpOne + dueNext
                nextDueNext = jumpTwo + dueLater
                nextDueLater = jumpThree
                nextMissed = missed + (1 if nextDueNow == 0 else 0)

                if nextMissed > 1:
                    continue

                coefficient = factorials[dueNow] // (
                    factorials[jumpOne]
                    * factorials[jumpTwo]
                    * factorials[jumpThree]
                )
                nextState = index[(nextDueNow, nextDueNext, nextDueLater, nextMissed)]
                matrix[stateNumber, nextState] = (
                    matrix[stateNumber, nextState] + coefficient
                ) % modulus

    return states, index, matrix


def frogTripsForModulus(roundTrips, squares, modulus):
    pathCount = 2 * roundTrips
    states, index, matrix = transitionMatrix(pathCount, modulus)
    vector = np.zeros(len(states), dtype=np.int64)
    vector[index[(pathCount, 0, 0, 0)]] = 1
    exponent = squares - 1

    while exponent:
        if exponent & 1:
            vector = (vector @ matrix) % modulus

        exponent //= 2

        if exponent:
            matrix = (matrix @ matrix) % modulus

    return int(
        (
            vector[index[(pathCount, 0, 0, 0)]]
            + vector[index[(pathCount, 0, 0, 1)]]
        )
        % modulus
    )


def frogTrips(roundTrips=TARGET_M, squares=TARGET_N):
    powerTwo = 2**9
    powerFive = 5**9
    residueTwo = frogTripsForModulus(roundTrips, squares, powerTwo)
    residueFive = frogTripsForModulus(roundTrips, squares, powerFive)
    coefficient = ((residueFive - residueTwo) * pow(powerTwo, -1, powerFive)) % powerFive

    return (residueTwo + powerTwo * coefficient) % MODULUS


def runTests():
    assert frogTrips(1, 3) == 4
    assert frogTrips(1, 4) == 15
    assert frogTrips(1, 5) == 46
    assert frogTrips(2, 3) == 16
    assert frogTrips(2, 100) == 429619151


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = frogTrips()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
