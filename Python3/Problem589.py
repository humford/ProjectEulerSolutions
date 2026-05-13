import time

import numpy as np


def expectedPlayTime(maxTime, minTime):
    cycleStart = minTime + 5
    cycleEnd = maxTime + 5
    cycleTimes = range(cycleStart, cycleEnd + 1)
    count = maxTime - minTime + 1
    countSquared = count * count

    # A[d] is the expected remaining time when neither stick is ahead and the
    # next emergence times differ by d. B[d] is the matching state where the
    # stick with the later next emergence is one completed trip ahead.
    stateCount = 2 * (cycleEnd + 1)

    def equalIndex(difference):
        return difference

    def leadingIndex(difference):
        return cycleEnd + 1 + difference

    matrix = np.eye(stateCount)
    constants = np.zeros(stateCount)

    for difference in range(1, cycleEnd + 1):
        row = equalIndex(difference)
        constant = 0.0
        for cycleTime in cycleTimes:
            if cycleTime < difference:
                constant += cycleTime
            elif cycleTime == difference:
                constant += difference
                matrix[row, leadingIndex(0)] -= 1 / count
            else:
                constant += difference
                matrix[row, leadingIndex(cycleTime - difference)] -= 1 / count
        constants[row] = constant / count

    for difference in range(1, cycleEnd + 1):
        row = leadingIndex(difference)
        constant = 0.0
        for cycleTime in cycleTimes:
            constant += min(difference, cycleTime)
            matrix[row, equalIndex(abs(difference - cycleTime))] -= 1 / count
        constants[row] = constant / count

    row = equalIndex(0)
    constant = 0.0
    for firstCycle in cycleTimes:
        for secondCycle in cycleTimes:
            constant += min(firstCycle, secondCycle)
            matrix[row, equalIndex(abs(firstCycle - secondCycle))] -= 1 / countSquared
    constants[row] = constant / countSquared

    row = leadingIndex(0)
    constant = 0.0
    for firstCycle in cycleTimes:
        for secondCycle in cycleTimes:
            constant += min(firstCycle, secondCycle)
            if firstCycle > secondCycle:
                matrix[row, leadingIndex(firstCycle - secondCycle)] -= 1 / countSquared
            elif firstCycle == secondCycle:
                matrix[row, leadingIndex(0)] -= 1 / countSquared
    constants[row] = constant / countSquared

    expectedStateTimes = np.linalg.solve(matrix, constants)

    total = 0.0
    for firstTime in range(minTime, maxTime + 1):
        for secondTime in range(minTime, maxTime + 1):
            total += (
                min(firstTime, secondTime)
                + expectedStateTimes[equalIndex(abs(firstTime - secondTime))]
            )

    return total / countSquared


def poohsticksSum(limit):
    return sum(
        expectedPlayTime(maxTime, minTime)
        for maxTime in range(2, limit + 1)
        for minTime in range(1, maxTime)
    )


def runTests():
    assert abs(expectedPlayTime(60, 30) - 1036.15479277899) < 1e-9
    assert format(expectedPlayTime(60, 30), ".2f") == "1036.15"
    assert format(poohsticksSum(5), ".2f") == "7722.82"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(poohsticksSum(100), ".2f")
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
