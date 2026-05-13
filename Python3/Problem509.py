import time


MODULUS = 1_234_567_890


def grundyValue(stones):
    if stones == 0:
        raise ValueError("Pile size must be positive")

    value = 0
    while stones % 2 == 0:
        value += 1
        stones //= 2

    return value


def grundyCounts(limit):
    counts = []
    power = 1

    while power <= limit:
        counts.append(limit // power - limit // (2 * power))
        power *= 2

    return counts


def losingPositionCount(limit):
    counts = grundyCounts(limit)
    total = 0

    for first, firstCount in enumerate(counts):
        for second, secondCount in enumerate(counts):
            third = first ^ second
            if third < len(counts):
                total += firstCount * secondCount * counts[third]

    return total


def winningPositionCount(limit, modulus=None):
    totalPositions = limit**3
    losingPositions = losingPositionCount(limit)
    result = totalPositions - losingPositions

    if modulus is not None:
        result %= modulus

    return result


def runTests():
    assert [grundyValue(n) for n in range(1, 17)] == [
        0,
        1,
        0,
        2,
        0,
        1,
        0,
        3,
        0,
        1,
        0,
        2,
        0,
        1,
        0,
        4,
    ]
    assert winningPositionCount(10) == 692
    assert winningPositionCount(100) == 735_494


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningPositionCount(123_456_787_654_321, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
