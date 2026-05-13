import time
from itertools import product
from math import factorial


def boundedStates(length, maxSum):
    states = []

    def addStates(prefix, remaining, slots):
        if slots == 0:
            states.append(tuple(prefix))
            return

        for value in range(remaining + 1):
            prefix.append(value)
            addStates(prefix, remaining - value, slots - 1)
            prefix.pop()

    addStates([], maxSum, length)
    return states


def survivalCoefficients(groupSize, window, days):
    blockLength = window + 1
    maxBlockPeople = groupSize - 1
    historyLength = blockLength - 1
    maxPeople = days * maxBlockPeople // blockLength

    states = boundedStates(historyLength, maxBlockPeople)
    stateIndexes = {state: index for index, state in enumerate(states)}
    inverseFactorials = [1 / factorial(count) for count in range(maxBlockPeople + 1)]
    transitions = []

    for state in states:
        stateTransitions = []
        stateTotal = sum(state)
        for newCount in range(maxBlockPeople - stateTotal + 1):
            nextState = state[1:] + (newCount,) if historyLength else ()
            stateTransitions.append((stateIndexes[nextState], newCount, inverseFactorials[newCount]))
        transitions.append(stateTransitions)

    coefficients = [0.0] * (maxPeople + 1)
    for startState in range(len(states)):
        current = {startState: [1.0] + [0.0] * maxPeople}

        for _ in range(days):
            nextValues = {}
            for state, polynomial in current.items():
                for nextState, newCount, weight in transitions[state]:
                    target = nextValues.get(nextState)
                    if target is None:
                        target = [0.0] * (maxPeople + 1)
                        nextValues[nextState] = target

                    limit = maxPeople + 1 - newCount
                    for degree in range(limit):
                        value = polynomial[degree]
                        if value:
                            target[degree + newCount] += value * weight

            current = nextValues

        finalPolynomial = current.get(startState)
        if finalPolynomial:
            for degree, value in enumerate(finalPolynomial):
                coefficients[degree] += value

    return coefficients


def expectedStoppingPeople(groupSize, window, days):
    expectation = 0.0
    factorialTerm = 1.0
    dayPower = 1.0

    for people, coefficient in enumerate(survivalCoefficients(groupSize, window, days)):
        if people > 0:
            factorialTerm *= people
            dayPower *= days

        expectation += coefficient * factorialTerm / dayPower

    return expectation


def birthdayExpectation(groupSize, window, days):
    return format(expectedStoppingPeople(groupSize, window, days), ".8f")


def hasCloseGroup(birthdays, groupSize, window, days):
    counts = [0] * days
    for birthday in birthdays:
        counts[birthday] += 1

    for start in range(days):
        if sum(counts[(start + offset) % days] for offset in range(window + 1)) >= groupSize:
            return True

    return False


def bruteExpectedStoppingPeople(groupSize, window, days):
    maxPeople = days * (groupSize - 1) // (window + 1)
    expectation = 0.0

    for people in range(maxPeople + 1):
        safeSequences = 0
        for birthdays in product(range(days), repeat=people):
            if not hasCloseGroup(birthdays, groupSize, window, days):
                safeSequences += 1

        expectation += safeSequences / (days ** people)

    return expectation


def runTests():
    brute = bruteExpectedStoppingPeople(3, 1, 5)
    generated = expectedStoppingPeople(3, 1, 5)
    assert abs(brute - generated) < 10 ** -12

    assert birthdayExpectation(3, 1, 10) == "5.78688636"
    assert birthdayExpectation(3, 7, 100) == "8.48967364"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = birthdayExpectation(4, 7, 365)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
