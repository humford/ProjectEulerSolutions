import time


MODULUS = 1_000_000_000
MOVES = (2, 3, 5, 7)
GRUNDY_PERIOD = (0, 0, 1, 1, 2, 2, 3, 3, 4)


def oneDimensionalGrundyValues(limit):
    values = []
    for position in range(limit):
        seen = {values[position - move] for move in MOVES if position >= move}
        grundy = 0
        while grundy in seen:
            grundy += 1
        values.append(grundy)
    return values


def coordinateGrundyCounts(size):
    periodLength = len(GRUNDY_PERIOD)
    cycles, remainder = divmod(size, periodLength)
    counts = {}
    for grundy in GRUNDY_PERIOD:
        counts[grundy] = counts.get(grundy, 0) + cycles
    for grundy in GRUNDY_PERIOD[:remainder]:
        counts[grundy] = counts.get(grundy, 0) + 1
    return counts


def squareGrundyCounts(size):
    coordinateCounts = coordinateGrundyCounts(size)
    counts = {}
    for first, firstCount in coordinateCounts.items():
        for second, secondCount in coordinateCounts.items():
            grundy = first ^ second
            counts[grundy] = (counts.get(grundy, 0) + firstCount * secondCount) % MODULUS
    return counts


def winningArrangementCount(size, coins):
    squareCounts = squareGrundyCounts(size)
    xorCounts = {0: 1}
    for _ in range(coins):
        nextCounts = {}
        for currentXor, currentCount in xorCounts.items():
            for squareGrundy, squareCount in squareCounts.items():
                newXor = currentXor ^ squareGrundy
                nextCounts[newXor] = (
                    nextCounts.get(newXor, 0) + currentCount * squareCount
                ) % MODULUS
        xorCounts = nextCounts

    return sum(count for xorValue, count in xorCounts.items() if xorValue) % MODULUS


def runTests():
    assert tuple(oneDimensionalGrundyValues(18)) == GRUNDY_PERIOD * 2
    assert winningArrangementCount(3, 1) == 4
    assert winningArrangementCount(3, 2) == 40
    assert winningArrangementCount(9, 3) == 450_304


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningArrangementCount(10_000_019, 100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
