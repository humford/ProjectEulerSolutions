import time


def cardPositions(cardCount):
    modulus = cardCount + 1
    positions = [0] * (cardCount + 1)
    value = 1

    for position in range(1, cardCount + 1):
        value = value * 3 % modulus
        if value == 0 or positions[value] != 0:
            raise ValueError("G(" + str(cardCount) + ") is not defined")
        positions[value] = position

    if any(position == 0 for position in positions[1:]):
        raise ValueError("G(" + str(cardCount) + ") is not defined")

    return positions


def optimalStackingDistance(cardCount):
    positions = cardPositions(cardCount)
    distances = [[0] * (cardCount + 1) for _ in range(cardCount + 1)]

    for right in range(2, cardCount + 1):
        rightPosition = positions[right]
        currentColumn = [0] * (right + 2)

        for left in range(right - 1, 0, -1):
            row = distances[left]
            best = 10 ** 18

            for split in range(left, right):
                value = (
                    row[split]
                    + currentColumn[split + 1]
                    + abs(positions[split] - rightPosition)
                )
                if value < best:
                    best = value

            row[right] = best
            currentColumn[left] = best

    return distances[1][cardCount]


def runTests():
    assert cardPositions(6)[1:] == [6, 2, 1, 4, 5, 3]
    assert optimalStackingDistance(6) == 8
    assert optimalStackingDistance(16) == 47


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = optimalStackingDistance(976)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
