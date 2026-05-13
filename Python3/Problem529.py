import functools
import time
from collections import deque


MODULUS = 1_000_000_007
INITIAL_STATE = ((10,), ())


def _friendly(number):
    digits = [int(digit) for digit in str(number)]
    covered = [False] * len(digits)
    for start in range(len(digits)):
        total = 0
        for end in range(start, len(digits)):
            total += digits[end]
            if total == 10:
                for index in range(start, end + 1):
                    covered[index] = True
            if total > 10:
                break
    return all(covered)


def smallFriendlyCount(n):
    return sum(1 for value in range(1, 10 ** n + 1) if _friendly(value))


def transition(state, digit):
    activeTargets, pendingTargets = state
    activeTargets = tuple(
        sorted(target - digit for target in activeTargets if target - digit >= 0)
    )

    if 0 in activeTargets:
        pendingTargets = tuple(
            sorted(target - digit for target in pendingTargets if target - digit >= 0)
        )
        return (tuple(sorted(set(activeTargets) | set(pendingTargets) | {10})), ())

    if not activeTargets:
        return None

    pendingTargets = set(
        target - digit for target in pendingTargets if target - digit >= 0
    )
    pendingTargets.add(10)
    return (activeTargets, tuple(sorted(pendingTargets)))


def buildAutomaton():
    states = [INITIAL_STATE]
    stateIndex = {INITIAL_STATE: 0}
    queue = deque([INITIAL_STATE])

    while queue:
        state = queue.popleft()
        for digit in range(10):
            nextState = transition(state, digit)
            if nextState is not None and nextState not in stateIndex:
                stateIndex[nextState] = len(states)
                states.append(nextState)
                queue.append(nextState)

    transitions = []
    for state in states:
        transitions.append(
            [
                stateIndex[transition(state, digit)]
                if transition(state, digit) is not None
                else -1
                for digit in range(10)
            ]
        )

    accepting = [not pendingTargets for _, pendingTargets in states]
    return stateIndex, transitions, accepting


def friendlyPrefixCounts(termCount):
    stateIndex, transitions, accepting = buildAutomaton()
    counts = [0] * len(transitions)

    for firstDigit in range(1, 10):
        nextState = transition(INITIAL_STATE, firstDigit)
        if nextState is not None:
            counts[stateIndex[nextState]] += 1

    sequence = []
    runningTotal = 0
    for _ in range(termCount):
        lengthCount = sum(
            count for index, count in enumerate(counts) if accepting[index]
        ) % MODULUS
        runningTotal = (runningTotal + lengthCount) % MODULUS
        sequence.append(runningTotal)

        nextCounts = [0] * len(counts)
        for index, count in enumerate(counts):
            if count:
                for nextIndex in transitions[index]:
                    if nextIndex >= 0:
                        nextCounts[nextIndex] = (
                            nextCounts[nextIndex] + count
                        ) % MODULUS
        counts = nextCounts

    return sequence


def berlekampMassey(sequence):
    current = [1]
    previous = [1]
    length = 0
    shift = 1
    lastDiscrepancy = 1

    for index in range(len(sequence)):
        discrepancy = sequence[index]
        for offset in range(1, length + 1):
            discrepancy = (
                discrepancy + current[offset] * sequence[index - offset]
            ) % MODULUS

        if discrepancy == 0:
            shift += 1
            continue

        oldCurrent = current[:]
        coefficient = discrepancy * pow(lastDiscrepancy, MODULUS - 2, MODULUS)
        if len(current) < len(previous) + shift:
            current += [0] * (len(previous) + shift - len(current))

        for offset, value in enumerate(previous):
            current[offset + shift] = (
                current[offset + shift] - coefficient * value
            ) % MODULUS

        if 2 * length <= index:
            length = index + 1 - length
            previous = oldCurrent
            lastDiscrepancy = discrepancy
            shift = 1
        else:
            shift += 1

    recurrence = [(MODULUS - coefficient) % MODULUS for coefficient in current[1:]]
    return recurrence


def combinePolynomials(left, right, recurrence):
    degree = len(recurrence)
    product = [0] * (2 * degree - 1)

    for leftIndex, leftValue in enumerate(left):
        if leftValue:
            for rightIndex, rightValue in enumerate(right):
                if rightValue:
                    product[leftIndex + rightIndex] = (
                        product[leftIndex + rightIndex] + leftValue * rightValue
                    ) % MODULUS

    for index in range(2 * degree - 2, degree - 1, -1):
        coefficient = product[index]
        if coefficient:
            base = index - degree
            for recurrenceIndex, recurrenceValue in enumerate(recurrence):
                target = base + degree - 1 - recurrenceIndex
                product[target] = (
                    product[target] + coefficient * recurrenceValue
                ) % MODULUS

    return product[:degree]


def linearRecurrenceValue(initialValues, recurrence, index):
    if index < len(initialValues):
        return initialValues[index]

    degree = len(recurrence)
    resultPolynomial = [0] * degree
    resultPolynomial[0] = 1
    powerPolynomial = [0] * degree
    powerPolynomial[1] = 1

    while index:
        if index % 2:
            resultPolynomial = combinePolynomials(
                resultPolynomial, powerPolynomial, recurrence
            )
        powerPolynomial = combinePolynomials(powerPolynomial, powerPolynomial, recurrence)
        index //= 2

    return sum(
        coefficient * initialValues[offset]
        for offset, coefficient in enumerate(resultPolynomial)
    ) % MODULUS


@functools.cache
def recurrenceData():
    stateCount = len(buildAutomaton()[1])
    sequence = friendlyPrefixCounts(2 * stateCount + 500)
    recurrence = berlekampMassey(sequence)
    degree = len(recurrence)

    for index in range(degree, len(sequence)):
        predicted = sum(
            recurrence[offset] * sequence[index - 1 - offset]
            for offset in range(degree)
        ) % MODULUS
        assert predicted == sequence[index]

    return sequence[:degree], recurrence


def friendlyCount(n):
    if n <= 7:
        return smallFriendlyCount(n)

    initialValues, recurrence = recurrenceData()
    return linearRecurrenceValue(initialValues, recurrence, n - 1)


def runTests():
    assert _friendly(3_523_014)
    assert not _friendly(28_546)
    assert friendlyCount(2) == 9
    assert friendlyCount(5) == 3_492
    assert friendlyCount(6) == 23_697


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = friendlyCount(10 ** 18) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
