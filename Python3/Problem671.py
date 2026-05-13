import time


MODULUS = 1_000_004_321


def nextIncomingState(rowState):
    if rowState == 1:
        return 0
    if rowState == 2:
        return 1
    raise ValueError("row state is not incoming")


def nextLengthState(length):
    return length - 1


def normalizeColours(fixedCount, topColour, bottomColour):
    mapping = {}
    nextLabel = fixedCount

    def normalize(colour):
        nonlocal nextLabel
        if colour < fixedCount:
            return colour
        if colour not in mapping:
            mapping[colour] = nextLabel
            nextLabel += 1
        return mapping[colour]

    return normalize(topColour), normalize(bottomColour)


def validState(state):
    previousVertical, topState, bottomState, topColour, bottomColour = state
    if topState not in (0, 1, 2) or bottomState not in (0, 1, 2):
        return False
    if previousVertical:
        return topState == 0 and bottomState == 0 and topColour == bottomColour
    return topColour != bottomColour


def transitionsFrom(state, colourCount, fixedCount):
    previousVertical, topState, bottomState, topColour, bottomColour = state
    if not validState(state):
        return {}

    inTop = topState != 0
    inBottom = bottomState != 0
    otherColours = sorted(
        {
            colour
            for colour in (topColour, bottomColour)
            if colour >= fixedCount
        }
    )
    unusedOther = colourCount - fixedCount - len(otherColours)
    existingColours = list(range(fixedCount)) + otherColours
    transitions = {}

    def add(currentVertical, nextTop, nextBottom, newTop, newBottom, weight):
        if weight <= 0:
            return
        if previousVertical == 0 and currentVertical == 0 and not inTop and not inBottom:
            return
        if currentVertical and (nextTop != 0 or nextBottom != 0):
            return
        normalizedTop, normalizedBottom = normalizeColours(
            fixedCount,
            newTop,
            newBottom,
        )
        nextState = (
            currentVertical,
            nextTop,
            nextBottom,
            normalizedTop,
            normalizedBottom,
        )
        transitions[nextState] = (transitions.get(nextState, 0) + weight) % MODULUS

    def singleChoices(forbidden):
        forbidden = set(forbidden)
        for colour in existingColours:
            if colour not in forbidden:
                yield colour, 1, False
        if unusedOther > 0:
            yield -1, unusedOther, True

    def pairChoices(forbiddenTop, forbiddenBottom):
        forbiddenTop = set(forbiddenTop)
        forbiddenBottom = set(forbiddenBottom)
        topExisting = [
            colour
            for colour in existingColours
            if colour not in forbiddenTop
        ]
        bottomExisting = [
            colour
            for colour in existingColours
            if colour not in forbiddenBottom
        ]

        for top in topExisting:
            for bottom in bottomExisting:
                if top != bottom:
                    yield top, bottom, 1
        if unusedOther > 0:
            for top in topExisting:
                yield top, -1, unusedOther
            for bottom in bottomExisting:
                yield -1, bottom, unusedOther
            if unusedOther > 1:
                yield -1, -1, unusedOther * (unusedOther - 1)

    if inTop and inBottom:
        add(
            0,
            nextIncomingState(topState),
            nextIncomingState(bottomState),
            topColour,
            bottomColour,
            1,
        )
        return transitions

    if inTop and not inBottom:
        nextTop = nextIncomingState(topState)
        for colour, weight, isNew in singleChoices({bottomColour, topColour}):
            placedColour = fixedCount + len(otherColours) if isNew else colour
            for length in (1, 2, 3):
                add(
                    0,
                    nextTop,
                    nextLengthState(length),
                    topColour,
                    placedColour,
                    weight,
                )
        return transitions

    if inBottom and not inTop:
        nextBottom = nextIncomingState(bottomState)
        for colour, weight, isNew in singleChoices({topColour, bottomColour}):
            placedColour = fixedCount + len(otherColours) if isNew else colour
            for length in (1, 2, 3):
                add(
                    0,
                    nextLengthState(length),
                    nextBottom,
                    placedColour,
                    bottomColour,
                    weight,
                )
        return transitions

    for colour, weight, isNew in singleChoices({topColour, bottomColour}):
        placedColour = fixedCount + len(otherColours) if isNew else colour
        add(1, 0, 0, placedColour, placedColour, weight)

    for topLength in (1, 2, 3):
        for bottomLength in (1, 2, 3):
            for top, bottom, weight in pairChoices({topColour}, {bottomColour}):
                topPlaced = fixedCount + len(otherColours) if top == -1 else top
                if bottom == -1:
                    bottomPlaced = (
                        fixedCount + len(otherColours) + 1
                        if top == -1
                        else fixedCount + len(otherColours)
                    )
                else:
                    bottomPlaced = bottom
                add(
                    0,
                    nextLengthState(topLength),
                    nextLengthState(bottomLength),
                    topPlaced,
                    bottomPlaced,
                    weight,
                )

    return transitions


def buildMatrix(colourCount, fixedCount, startStates):
    states = []
    stateIndex = {}
    queue = []

    for state in startStates:
        topColour, bottomColour = normalizeColours(fixedCount, state[3], state[4])
        normalized = (state[0], state[1], state[2], topColour, bottomColour)
        if validState(normalized) and normalized not in stateIndex:
            stateIndex[normalized] = len(states)
            states.append(normalized)
            queue.append(normalized)

    queueIndex = 0
    while queueIndex < len(queue):
        state = queue[queueIndex]
        queueIndex += 1
        for nextState in transitionsFrom(state, colourCount, fixedCount):
            if nextState not in stateIndex:
                stateIndex[nextState] = len(states)
                states.append(nextState)
                queue.append(nextState)

    matrix = [[0] * len(states) for _ in states]
    for state in states:
        row = stateIndex[state]
        for nextState, weight in transitionsFrom(state, colourCount, fixedCount).items():
            column = stateIndex[nextState]
            matrix[row][column] = (matrix[row][column] + weight) % MODULUS
    return matrix, stateIndex


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


def matrixPower(matrix, exponent):
    size = len(matrix)
    result = [
        [1 if row == column else 0 for column in range(size)]
        for row in range(size)
    ]
    power = matrix
    while exponent:
        if exponent & 1:
            result = multiplyMatrices(result, power)
        exponent //= 2
        if exponent:
            power = multiplyMatrices(power, power)
    return result


def modularInverse(value):
    oldRemainder, remainder = MODULUS, value % MODULUS
    oldCoefficient, coefficient = 0, 1
    while remainder:
        quotient = oldRemainder // remainder
        oldRemainder, remainder = (
            remainder,
            oldRemainder - quotient * remainder,
        )
        oldCoefficient, coefficient = (
            coefficient,
            oldCoefficient - quotient * coefficient,
        )
    if oldRemainder != 1:
        raise ValueError("modular inverse does not exist")
    return oldCoefficient % MODULUS


def loopColouringCount(colourCount, length):
    sameStart = (1, 0, 0, 0, 0)
    sameMatrix, sameIndex = buildMatrix(colourCount, 1, [sameStart])
    samePower = matrixPower(sameMatrix, length)
    sameCount = samePower[sameIndex[sameStart]][sameIndex[sameStart]]

    differentStarts = [
        (0, topState, bottomState, 0, 1)
        for topState in (0, 1, 2)
        for bottomState in (0, 1, 2)
    ]
    differentMatrix, differentIndex = buildMatrix(
        colourCount,
        2,
        differentStarts,
    )
    differentPower = matrixPower(differentMatrix, length)
    differentCount = 0
    for state in differentStarts:
        if state in differentIndex:
            index = differentIndex[state]
            differentCount = (differentCount + differentPower[index][index]) % MODULUS

    markedCount = (
        colourCount * sameCount
        + colourCount * (colourCount - 1) * differentCount
    ) % MODULUS
    return markedCount * modularInverse(length) % MODULUS


def runTests():
    assert loopColouringCount(4, 3) == 104
    assert loopColouringCount(5, 7) == 3_327_300
    assert loopColouringCount(6, 101) == 75_309_980


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = loopColouringCount(10, 10_004_003_002_001)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
