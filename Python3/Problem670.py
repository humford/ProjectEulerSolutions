import time


MODULUS = 1_000_004_321
COLOURS = 4
NO_COLOUR = 4
INITIAL_STATE = (1, 0, 0, NO_COLOUR, 0, 0, NO_COLOUR)


def transitionsFrom(state):
    previousVertical, inTop, contTop, topValue, inBottom, contBottom, bottomValue = state
    transitions = {}

    def add(currentVertical, topState, bottomState, ways):
        if previousVertical == 0 and currentVertical == 0 and inTop == 0 and inBottom == 0:
            return
        nextState = (currentVertical, *topState, *bottomState)
        transitions[nextState] = (transitions.get(nextState, 0) + ways) % MODULUS

    def advanceIncoming(incoming, continues, colour):
        if incoming == 0:
            raise ValueError("row is not incoming")
        if continues:
            return (1, 0, colour)
        return (0, 0, colour)

    topColour = topValue if inTop else -1
    bottomColour = bottomValue if inBottom else -1
    nextTop = advanceIncoming(inTop, contTop, topValue) if inTop else None
    nextBottom = advanceIncoming(inBottom, contBottom, bottomValue) if inBottom else None

    if inTop and inBottom:
        if topColour != bottomColour:
            add(0, nextTop, nextBottom, 1)
        return transitions

    if inTop and not inBottom:
        for length in [1, 2, 3]:
            for colour in range(COLOURS):
                if bottomValue != NO_COLOUR and colour == bottomValue:
                    continue
                if colour == topColour:
                    continue
                bottomState = (0, 0, colour)
                if length == 2:
                    bottomState = (1, 0, colour)
                elif length == 3:
                    bottomState = (1, 1, colour)
                add(0, nextTop, bottomState, 1)
        return transitions

    if not inTop and inBottom:
        for length in [1, 2, 3]:
            for colour in range(COLOURS):
                if topValue != NO_COLOUR and colour == topValue:
                    continue
                if colour == bottomColour:
                    continue
                topState = (0, 0, colour)
                if length == 2:
                    topState = (1, 0, colour)
                elif length == 3:
                    topState = (1, 1, colour)
                add(0, topState, nextBottom, 1)
        return transitions

    for colour in range(COLOURS):
        if topValue != NO_COLOUR and colour == topValue:
            continue
        if bottomValue != NO_COLOUR and colour == bottomValue:
            continue
        add(1, (0, 0, colour), (0, 0, colour), 1)

    for topLength in [1, 2, 3]:
        for bottomLength in [1, 2, 3]:
            for topColourChoice in range(COLOURS):
                if topValue != NO_COLOUR and topColourChoice == topValue:
                    continue
                for bottomColourChoice in range(COLOURS):
                    if bottomValue != NO_COLOUR and bottomColourChoice == bottomValue:
                        continue
                    if topColourChoice == bottomColourChoice:
                        continue

                    topState = (0, 0, topColourChoice)
                    if topLength == 2:
                        topState = (1, 0, topColourChoice)
                    elif topLength == 3:
                        topState = (1, 1, topColourChoice)

                    bottomState = (0, 0, bottomColourChoice)
                    if bottomLength == 2:
                        bottomState = (1, 0, bottomColourChoice)
                    elif bottomLength == 3:
                        bottomState = (1, 1, bottomColourChoice)

                    add(0, topState, bottomState, 1)

    return transitions


def buildAutomaton():
    states = [INITIAL_STATE]
    stateIndex = {INITIAL_STATE: 0}
    adjacency = []
    queueIndex = 0

    while queueIndex < len(states):
        state = states[queueIndex]
        queueIndex += 1
        row = []
        for nextState, weight in transitionsFrom(state).items():
            if nextState not in stateIndex:
                stateIndex[nextState] = len(states)
                states.append(nextState)
            row.append((stateIndex[nextState], weight))
        adjacency.append(row)

    return states, adjacency


def smallColouringCount(length, states, adjacency):
    stateIndex = {state: index for index, state in enumerate(states)}
    values = [0] * len(states)
    values[stateIndex[INITIAL_STATE]] = 1

    for _ in range(length):
        nextValues = [0] * len(states)
        for index, value in enumerate(values):
            if value == 0:
                continue
            for nextIndex, weight in adjacency[index]:
                nextValues[nextIndex] = (
                    nextValues[nextIndex] + value * weight
                ) % MODULUS
        values = nextValues

    return finishedStateTotal(values, states)


def finishedStateTotal(values, states):
    total = 0
    for value, state in zip(values, states):
        _, inTop, _, _, inBottom, _, _ = state
        if inTop == 0 and inBottom == 0:
            total = (total + value) % MODULUS
    return total


def denseMatrix(adjacency):
    size = len(adjacency)
    matrix = [[0] * size for _ in range(size)]
    for index, row in enumerate(adjacency):
        for nextIndex, weight in row:
            matrix[index][nextIndex] = weight
    return matrix


def multiplyMatrices(left, right):
    size = len(left)
    result = [[0] * size for _ in range(size)]
    for rowIndex in range(size):
        row = left[rowIndex]
        resultRow = result[rowIndex]
        for middle in range(size):
            value = row[middle]
            if value == 0:
                continue
            rightRow = right[middle]
            for column in range(size):
                resultRow[column] += value * rightRow[column]
        for column in range(size):
            resultRow[column] %= MODULUS
    return result


def multiplyVector(vector, matrix):
    result = [0] * len(vector)
    for index, value in enumerate(vector):
        if value == 0:
            continue
        for column, weight in enumerate(matrix[index]):
            if weight:
                result[column] = (result[column] + value * weight) % MODULUS
    return result


def applyPower(matrix, exponent, vector):
    result = vector[:]
    power = matrix
    while exponent:
        if exponent & 1:
            result = multiplyVector(result, power)
        exponent //= 2
        if exponent:
            power = multiplyMatrices(power, power)
    return result


def stripColouringCount(length):
    states, adjacency = buildAutomaton()
    assert smallColouringCount(2, states, adjacency) == 120
    assert smallColouringCount(5, states, adjacency) == 45_876
    assert smallColouringCount(100, states, adjacency) == 53_275_818

    stateIndex = {state: index for index, state in enumerate(states)}
    initial = [0] * len(states)
    initial[stateIndex[INITIAL_STATE]] = 1
    values = applyPower(denseMatrix(adjacency), length, initial)
    return finishedStateTotal(values, states)


def runTests():
    assert stripColouringCount(2) == 120
    assert stripColouringCount(5) == 45_876
    assert stripColouringCount(100) == 53_275_818


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = stripColouringCount(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
