from functools import cache
import time


MODULUS = 1_000_000_007


def canonical(labels):
    mapping = {}
    nextLabel = 0
    result = []

    for label in labels:
        if label not in mapping:
            mapping[label] = nextLabel
            nextLabel += 1
        result.append(mapping[label])

    return tuple(result)


def addPolynomial(target, state, polynomial, sign=1):
    values = target.get(state)
    if values is None:
        target[state] = [(sign * value) % MODULUS for value in polynomial]
        return

    if len(values) < len(polynomial):
        values.extend([0] * (len(polynomial) - len(values)))

    if sign == 1:
        for index, value in enumerate(polynomial):
            values[index] = (values[index] + value) % MODULUS
    else:
        for index, value in enumerate(polynomial):
            values[index] = (values[index] - value) % MODULUS


def unionState(state, first, second):
    if state[first] == state[second]:
        return None

    source = state[second]
    target = state[first]
    return canonical(target if label == source else label for label in state)


@cache
def chromaticPolynomial(rows, cols):
    vertexOrder = [(col, row) for col in range(cols) for row in range(rows)]
    vertexIndex = {vertex: index for index, vertex in enumerate(vertexOrder)}
    activeVertices = []
    states = {(): [1]}

    def hasFutureEdge(vertex, currentIndex):
        col, row = vertex
        neighbours = (
            (col - 1, row),
            (col + 1, row),
            (col, row - 1),
            (col, row + 1),
        )
        return any(
            neighbour in vertexIndex and vertexIndex[neighbour] > currentIndex
            for neighbour in neighbours
        )

    for currentIndex, vertex in enumerate(vertexOrder):
        activeVertices.append(vertex)
        states = {
            state + ((max(state) + 1) if state else 0,): polynomial
            for state, polynomial in states.items()
        }

        col, row = vertex
        for neighbour in ((col - 1, row), (col, row - 1)):
            if neighbour not in activeVertices:
                continue

            first = activeVertices.index(neighbour)
            second = activeVertices.index(vertex)
            nextStates = {}

            for state, polynomial in states.items():
                joinedState = unionState(state, first, second)
                if joinedState is None:
                    continue

                addPolynomial(nextStates, state, polynomial, 1)
                addPolynomial(nextStates, joinedState, polynomial, -1)

            states = nextStates

        changed = True
        while changed:
            changed = False
            for forgottenIndex, forgottenVertex in list(enumerate(activeVertices)):
                if hasFutureEdge(forgottenVertex, currentIndex):
                    continue

                nextStates = {}
                for state, polynomial in states.items():
                    label = state[forgottenIndex]
                    nextState = canonical(
                        state[:forgottenIndex] + state[forgottenIndex + 1 :]
                    )
                    if state.count(label) == 1:
                        nextPolynomial = [0] + polynomial
                    else:
                        nextPolynomial = polynomial
                    addPolynomial(nextStates, nextState, nextPolynomial, 1)

                activeVertices.pop(forgottenIndex)
                states = nextStates
                changed = True
                break

    return tuple(next(iter(states.values())))


def evaluatePolynomial(polynomial, value):
    result = 0
    for coefficient in reversed(polynomial):
        result = (result * value + coefficient) % MODULUS
    return result


def interpolateConsecutive(values, value):
    if value < len(values):
        return values[value]

    count = len(values)
    prefix = [1] * (count + 1)
    suffix = [1] * (count + 1)

    for index in range(count):
        prefix[index + 1] = prefix[index] * (value - index) % MODULUS
    for index in range(count - 1, -1, -1):
        suffix[index] = suffix[index + 1] * (value - index) % MODULUS

    factorial = [1] * count
    inverseFactorial = [1] * count
    for index in range(1, count):
        factorial[index] = factorial[index - 1] * index % MODULUS

    inverseFactorial[-1] = pow(factorial[-1], MODULUS - 2, MODULUS)
    for index in range(count - 2, -1, -1):
        inverseFactorial[index] = inverseFactorial[index + 1] * (index + 1) % MODULUS

    total = 0
    for index, yValue in enumerate(values):
        denominator = inverseFactorial[index] * inverseFactorial[count - 1 - index]
        if (count - 1 - index) % 2:
            denominator = -denominator
        total = (
            total
            + yValue * prefix[index] * suffix[index + 1] * denominator
        ) % MODULUS

    return total


def gridColourings(rows, cols, colours):
    return evaluatePolynomial(chromaticPolynomial(rows, cols), colours % MODULUS)


def gridColouringSum(rows, cols, colours):
    polynomial = chromaticPolynomial(rows, cols)
    prefixValues = []
    runningTotal = 0

    for colourCount in range(len(polynomial) + 1):
        if colourCount:
            runningTotal = (
                runningTotal + evaluatePolynomial(polynomial, colourCount)
            ) % MODULUS
        prefixValues.append(runningTotal)

    return interpolateConsecutive(prefixValues, colours % MODULUS)


def runTests():
    assert gridColourings(2, 2, 3) == 18
    assert gridColourings(2, 2, 20) == 130_340
    assert gridColourings(3, 4, 6) == 102_923_670
    assert gridColouringSum(4, 4, 15) % MODULUS == 325_951_319


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gridColouringSum(9, 10, 1_112_131_415) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
