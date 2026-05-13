import time
from array import array


GENERATOR_MODULUS = 50515093
SEED = 290797
TARGET = 2_000_000_000


def nextValue(value):
    return value * value % GENERATOR_MODULUS


def sequence(length):
    value = SEED
    values = []

    for _ in range(length):
        value = nextValue(value)
        values.append(value)

    return values


def periodValues():
    value = nextValue(SEED)
    firstValue = value
    values = array("I", [value])

    while True:
        value = nextValue(value)
        if value == firstValue:
            return values
        values.append(value)


def subsequenceMinimumSum(values):
    stack = []
    total = 0
    endingSum = 0

    for value in values:
        count = 1

        while stack and stack[-1][0] >= value:
            previousValue, previousCount = stack.pop()
            endingSum -= previousValue * previousCount
            count += previousCount

        stack.append((value, count))
        endingSum += value * count
        total += endingSum

    return total


def excessMinimumSum(values, globalMinimum):
    length = len(values)
    return subsequenceMinimumSum(values) - globalMinimum * length * (length + 1) // 2


def largeSubsequenceMinimumSum(limit=TARGET):
    values = periodValues()
    period = len(values)
    globalMinimum = min(values)
    minimumIndex = values.index(globalMinimum)

    assert values.count(globalMinimum) == 1

    firstMinimumPosition = minimumIndex + 1
    if limit < firstMinimumPosition:
        return subsequenceMinimumSum(values[:limit])

    minimumCount = (limit - firstMinimumPosition) // period + 1
    lastMinimumPosition = firstMinimumPosition + (minimumCount - 1) * period
    beforeFirstMinimum = values[:minimumIndex]
    betweenMinima = values[minimumIndex + 1 :] + values[:minimumIndex]
    afterLastMinimum = betweenMinima[: limit - lastMinimumPosition]

    total = globalMinimum * limit * (limit + 1) // 2
    total += excessMinimumSum(beforeFirstMinimum, globalMinimum)
    total += (minimumCount - 1) * excessMinimumSum(betweenMinima, globalMinimum)
    total += excessMinimumSum(afterLastMinimum, globalMinimum)
    return total


def runTests():
    assert subsequenceMinimumSum(sequence(10)) == 432256955
    assert subsequenceMinimumSum(sequence(10000)) == 3264567774119

    values = periodValues()
    assert len(values) == 6308948
    assert min(values) == 3
    assert values.count(3) == 1


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largeSubsequenceMinimumSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
