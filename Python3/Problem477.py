import time

import numpy as np


MODULUS = 1_000_000_007
PROBLEM_LENGTH = 10**8


def nextSequenceValue(value):
    return (value * value + 45) % MODULUS


def sequence(length):
    values = np.empty(length, dtype=np.int64)
    value = 0
    values[0] = value
    for index in range(1, length):
        value = nextSequenceValue(value)
        values[index] = value
    return values


def optimalFirstScore(values):
    count = len(values)
    differences = values.copy()
    total = int(values.sum(dtype=np.int64))

    for span in range(2, count + 1):
        remaining = count - span + 1
        leftChoice = values[:remaining] - differences[1:remaining + 1]
        rightChoice = values[span - 1:] - differences[:remaining]
        np.maximum(leftChoice, rightChoice, out=differences[:remaining])

    return (total + int(differences[0])) // 2


def smallOptimalFirstScore(values):
    values = list(values)
    total = sum(values)
    differences = values[:]
    count = len(values)
    for span in range(2, count + 1):
        for start in range(count - span + 1):
            end = start + span - 1
            differences[start] = max(
                values[start] - differences[start + 1],
                values[end] - differences[start],
            )
    return (total + differences[0]) // 2


def floydCycle():
    tortoise = nextSequenceValue(0)
    hare = nextSequenceValue(nextSequenceValue(0))
    while tortoise != hare:
        tortoise = nextSequenceValue(tortoise)
        hare = nextSequenceValue(nextSequenceValue(hare))

    start = 0
    tortoise = 0
    while tortoise != hare:
        tortoise = nextSequenceValue(tortoise)
        hare = nextSequenceValue(hare)
        start += 1

    length = 1
    hare = nextSequenceValue(tortoise)
    while tortoise != hare:
        hare = nextSequenceValue(hare)
        length += 1

    return start, length


def cyclePrefix(cycleStart, cycleLength):
    values = [0] * (cycleStart + cycleLength)
    value = 0
    values[0] = value
    for index in range(1, len(values)):
        value = nextSequenceValue(value)
        values[index] = value
    return values


def sequenceValueAt(index, values, cycleStart, cycleLength):
    zeroBased = index - 1
    if zeroBased < len(values):
        return values[zeroBased]
    return values[cycleStart + (zeroBased - cycleStart) % cycleLength]


def reducibleLength(length, period, values, cycleStart, cycleLength):
    reduced = length
    blocks = 0
    while reduced > period:
        if sequenceValueAt(reduced, values, cycleStart, cycleLength) != (
            sequenceValueAt(reduced - period, values, cycleStart, cycleLength)
        ):
            break

        reduced -= period
        blocks += 1

    return reduced, blocks


def repeatedBlockFirstPlayerGain(start, period, values, cycleStart, cycleLength):
    parity = start & 1
    total = 0
    for index in range(start, start + period):
        if index & 1 == parity:
            total += sequenceValueAt(index, values, cycleStart, cycleLength)
    return total


def sequenceGameScore(length):
    cycleStart, cycleLength = floydCycle()
    prefix = cyclePrefix(cycleStart, cycleLength)
    period = 8 * cycleLength
    reducedLength, blockCount = reducibleLength(
        length, period, prefix, cycleStart, cycleLength
    )
    baseScore = optimalFirstScore(sequence(reducedLength))
    blockGain = repeatedBlockFirstPlayerGain(
        reducedLength + 1, period, prefix, cycleStart, cycleLength
    )
    return baseScore + blockCount * blockGain


def runTests():
    values = sequence(10_000)
    assert smallOptimalFirstScore(values[:4]) == 4_284_990
    assert optimalFirstScore(values[:2]) == 45
    assert optimalFirstScore(values[:4]) == 4_284_990
    assert optimalFirstScore(values[:100]) == 26_365_463_243
    assert optimalFirstScore(values) == 2_495_838_522_951


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sequenceGameScore(PROBLEM_LENGTH)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
