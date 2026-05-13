import time


MODULUS = 1_000_000_123


def buildAutomaton():
    states = []
    stateIndex = {}
    for oddEvenDigits in range(6):
        for unseenOddDigits in range(6):
            for oddCountOddDigits in range(6 - unseenOddDigits):
                evenCountOddDigits = 5 - unseenOddDigits - oddCountOddDigits
                state = (oddEvenDigits, unseenOddDigits, oddCountOddDigits, evenCountOddDigits)
                stateIndex[state] = len(states)
                states.append(state)

    stateCount = len(states)
    totalIndex = stateCount
    transition = [[0] * (stateCount + 1) for _ in range(stateCount + 1)]

    def addTransition(source, target, count):
        transition[source][stateIndex[target]] += count
        transition[source][stateIndex[target]] %= MODULUS

    for index, (oddEven, unseenOdd, oddCountOdd, evenCountOdd) in enumerate(states):
        if 5 - oddEven:
            addTransition(index, (oddEven + 1, unseenOdd, oddCountOdd, evenCountOdd), 5 - oddEven)
        if oddEven:
            addTransition(index, (oddEven - 1, unseenOdd, oddCountOdd, evenCountOdd), oddEven)

        if unseenOdd:
            addTransition(index, (oddEven, unseenOdd - 1, oddCountOdd + 1, evenCountOdd), unseenOdd)
        if oddCountOdd:
            addTransition(index, (oddEven, unseenOdd, oddCountOdd - 1, evenCountOdd + 1), oddCountOdd)
        if evenCountOdd:
            addTransition(index, (oddEven, unseenOdd, oddCountOdd + 1, evenCountOdd - 1), evenCountOdd)

    validStates = [
        index
        for index, (oddEven, _unseenOdd, _oddCountOdd, evenCountOdd) in enumerate(states)
        if oddEven == 0 and evenCountOdd == 0
    ]
    for index in range(stateCount):
        transition[index][totalIndex] = sum(transition[index][valid] for valid in validStates) % MODULUS
    transition[totalIndex][totalIndex] = 1

    initial = [0] * (stateCount + 1)
    initial[stateIndex[(1, 5, 0, 0)]] = 4
    initial[stateIndex[(0, 4, 1, 0)]] = 5
    initial[totalIndex] = sum(initial[valid] for valid in validStates) % MODULUS

    return transition, initial, totalIndex


def advanceVector(vector, matrix):
    result = [0] * len(vector)
    for rowIndex, value in enumerate(vector):
        if value:
            row = matrix[rowIndex]
            for columnIndex, entry in enumerate(row):
                if entry:
                    result[columnIndex] = (result[columnIndex] + value * entry) % MODULUS
    return result


def multiplyMatrices(left, right):
    size = len(left)
    result = [[0] * size for _ in range(size)]
    for rowIndex, leftRow in enumerate(left):
        resultRow = result[rowIndex]
        for middleIndex, leftValue in enumerate(leftRow):
            if leftValue:
                rightRow = right[middleIndex]
                for columnIndex, rightValue in enumerate(rightRow):
                    if rightValue:
                        resultRow[columnIndex] = (resultRow[columnIndex] + leftValue * rightValue) % MODULUS
    return result


def simberCount(maxDigits):
    if maxDigits <= 0:
        return 0

    transition, vector, totalIndex = buildAutomaton()
    exponent = maxDigits - 1
    while exponent:
        if exponent & 1:
            vector = advanceVector(vector, transition)
        exponent //= 2
        if exponent:
            transition = multiplyMatrices(transition, transition)

    return vector[totalIndex]


def simberPowerSum(maxPower=39):
    transition, vector, totalIndex = buildAutomaton()
    powers = [transition]
    for _ in range(maxPower):
        powers.append(multiplyMatrices(powers[-1], powers[-1]))

    total = 0
    for power in range(1, maxPower + 1):
        vector = advanceVector(vector, powers[power - 1])
        total = (total + vector[totalIndex]) % MODULUS
    return total


def runTests():
    assert simberCount(7) == 287_975
    assert simberCount(100) == 123_864_868


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = simberPowerSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
