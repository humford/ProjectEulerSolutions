from functools import lru_cache
import time


LAST_ZERO = 0
LAST_ONE = 1
LIMIT = 45


def rudinShapiroValue(number):
    bits = bin(number)[2:]
    adjacentPairs = sum(1 for index in range(len(bits) - 1) if bits[index : index + 2] == "11")
    return 1 if adjacentPairs % 2 == 0 else -1


def childBlocks(lastBit, sign):
    if lastBit == LAST_ZERO:
        return ((LAST_ZERO, sign), (LAST_ONE, sign))

    return ((LAST_ZERO, sign), (LAST_ONE, -sign))


@lru_cache(maxsize=None)
def blockStats(lastBit, sign, length):
    if length == 0:
        return sign, sign, sign

    (firstLastBit, firstSign), (secondLastBit, secondSign) = childBlocks(lastBit, sign)
    firstTotal, firstMin, firstMax = blockStats(firstLastBit, firstSign, length - 1)
    secondTotal, secondMin, secondMax = blockStats(secondLastBit, secondSign, length - 1)

    return (
        firstTotal + secondTotal,
        min(firstMin, firstTotal + secondMin),
        max(firstMax, firstTotal + secondMax),
    )


@lru_cache(maxsize=None)
def blockOccurrenceCount(lastBit, sign, length, target):
    _total, minimum, maximum = blockStats(lastBit, sign, length)

    if target < minimum or target > maximum:
        return 0

    if length == 0:
        return 1 if target == sign else 0

    (firstLastBit, firstSign), (secondLastBit, secondSign) = childBlocks(lastBit, sign)
    firstTotal = blockStats(firstLastBit, firstSign, length - 1)[0]

    return blockOccurrenceCount(
        firstLastBit, firstSign, length - 1, target
    ) + blockOccurrenceCount(secondLastBit, secondSign, length - 1, target - firstTotal)


def findOccurrence(lastBit, sign, length, target, occurrence):
    if length == 0:
        return 0

    (firstLastBit, firstSign), (secondLastBit, secondSign) = childBlocks(lastBit, sign)
    firstTotal = blockStats(firstLastBit, firstSign, length - 1)[0]
    firstOccurrences = blockOccurrenceCount(firstLastBit, firstSign, length - 1, target)

    if occurrence <= firstOccurrences:
        return findOccurrence(firstLastBit, firstSign, length - 1, target, occurrence)

    return (1 << (length - 1)) + findOccurrence(
        secondLastBit,
        secondSign,
        length - 1,
        target - firstTotal,
        occurrence - firstOccurrences,
    )


def g(target, occurrence):
    length = 0

    while blockOccurrenceCount(LAST_ZERO, 1, length, target) < occurrence:
        length += 1

    return findOccurrence(LAST_ZERO, 1, length, target, occurrence)


def fibonacciValues(limit):
    values = [1, 1]

    while len(values) <= limit:
        values.append(values[-1] + values[-2])

    return values


def rudinShapiroFibonacciSum(limit=LIMIT):
    fibonacci = fibonacciValues(limit)
    return sum(g(fibonacci[index], fibonacci[index - 1]) for index in range(2, limit + 1))


def gSmall(target, occurrence):
    total = 0
    seen = 0
    number = 0

    while True:
        total += rudinShapiroValue(number)

        if total == target:
            seen += 1

            if seen == occurrence:
                return number

        number += 1


def runTests():
    assert [rudinShapiroValue(number) for number in range(8)] == [1, 1, 1, -1, 1, 1, -1, 1]
    assert gSmall(3, 3) == 6
    assert g(3, 3) == 6
    assert g(4, 2) == 7
    assert g(54321, 12345) == 1220847710


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rudinShapiroFibonacciSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
