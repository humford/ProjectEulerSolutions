import itertools
import time


START = (45, 90)


def r(point):
    x, y = point
    return x + 1, 2 * y


def s(point):
    x, y = point
    return 2 * x, y + 1


def applyOperations(start, operations):
    point = start
    states = [point]
    for operation in operations:
        if operation == "r":
            point = r(point)
        elif operation == "s":
            point = s(point)
        else:
            raise ValueError("Unknown operation: " + repr(operation))
        states.append(point)
    return states


def isPathToEquality(states):
    if not states:
        return False
    return all(x != y for x, y in states[:-1]) and states[-1][0] == states[-1][1]


def bruteForcePathExists(start, maxOperations):
    for operationCount in range(maxOperations + 1):
        for mask in range(1 << operationCount):
            operations = ["r" if (mask >> bit) & 1 else "s" for bit in range(operationCount)]
            if isPathToEquality(applyOperations(start, operations)):
                return True
    return False


def rightHandSideFromEarlyReverseRPositions(columnCount, positions):
    positionIndex = 0
    total = 0
    for column in range(columnCount):
        while positionIndex < len(positions) and positions[positionIndex] <= column:
            positionIndex += 1
        total += 1 << positionIndex
    return total


def smallestOddPathToEquality(start=START):
    # Work backwards from the unknown equality point. If there are t reverse-S
    # moves and t reverse-R moves, then 45 of the reverse-R moves are forced
    # into the last column; only t-45 early reverse-R moves remain to place.
    for columnCount in range(45, 200):
        earlyReverseRCount = columnCount - 45
        solutions = []

        for positions in itertools.combinations_with_replacement(range(columnCount), earlyReverseRCount):
            left = sum(1 << position for position in positions)
            right = rightHandSideFromEarlyReverseRPositions(columnCount, positions)
            if left == right:
                solutions.append(positions)

        if not solutions:
            continue

        assert len(solutions) == 1
        positions = solutions[0]

        reverseRCountsByColumn = [0] * (columnCount + 1)
        for position in positions:
            reverseRCountsByColumn[position] += 1
        reverseRCountsByColumn[columnCount] = 45

        reverseOperations = []
        for column in range(columnCount):
            reverseOperations.extend(["R"] * reverseRCountsByColumn[column])
            reverseOperations.append("S")
        reverseOperations.extend(["R"] * reverseRCountsByColumn[columnCount])

        forwardOperations = ["r" if operation == "R" else "s" for operation in reversed(reverseOperations)]
        states = applyOperations(start, forwardOperations)
        assert isPathToEquality(states)

        return len(states), states[-1][0], forwardOperations

    raise RuntimeError("No path found in the searched range")


def runTests():
    assert r((1, 1)) == (2, 2)
    assert s((1, 1)) == (2, 2)

    sampleOperations = list("rssssrsrr")
    sampleStates = applyOperations(START, sampleOperations)
    assert len(sampleStates) == 10
    assert sampleStates[-1] == (1476, 1476)
    assert isPathToEquality(sampleStates)
    assert not bruteForcePathExists(START, 8)


if __name__ == "__main__":
    runTests()
    start = time.time()
    pathLength, answer, _ = smallestOddPathToEquality()
    elapsed = time.time() - start

    print("Found " + str(answer) + " with path length " + str(pathLength) + " in " + str(elapsed) + " seconds.")
