import time


LIMIT = 10_000
MODULUS = 10**18


def nextOptionCounts(previousCounts, previousGrundy, beforeCounts, beforeGrundy):
    counts = {0: 1}

    for grundy, amount in previousCounts.items():
        nextGrundy = 1 + (grundy ^ beforeGrundy)
        counts[nextGrundy] = (counts.get(nextGrundy, 0) + amount) % MODULUS

    for grundy, amount in beforeCounts.items():
        nextGrundy = 1 + (previousGrundy ^ grundy)
        counts[nextGrundy] = (counts.get(nextGrundy, 0) + amount) % MODULUS

    return counts


def winningFirstMoves(limit=LIMIT):
    if limit == 1:
        return 0

    beforeGrundy = 0
    beforeCounts = {}
    previousGrundy = 1
    previousCounts = {0: 1}

    for _ in range(2, limit):
        currentCounts = nextOptionCounts(
            previousCounts,
            previousGrundy,
            beforeCounts,
            beforeGrundy,
        )
        currentGrundy = 1 + (previousGrundy ^ beforeGrundy)
        beforeGrundy, previousGrundy = previousGrundy, currentGrundy
        beforeCounts, previousCounts = previousCounts, currentCounts

    return (
        previousCounts.get(beforeGrundy, 0)
        + beforeCounts.get(previousGrundy, 0)
    ) % MODULUS


def runTests():
    assert winningFirstMoves(1) == 0
    assert winningFirstMoves(5) == 1
    assert winningFirstMoves(10) == 17


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningFirstMoves()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
