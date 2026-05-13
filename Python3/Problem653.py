import time


MARBLE_DIAMETER = 20
WEST_CENTER_LIMIT = 10
RANDOM_MODULUS = 32_745_673
EASTWARD_THRESHOLD = 10_000_000


def generatedMarbleData(marbleCount):
    value = 6_563_116
    compressedPosition = WEST_CENTER_LIMIT

    for _ in range(marbleCount):
        gap = value % 1000 + 1
        compressedPosition += gap
        yield compressedPosition, value <= EASTWARD_THRESHOLD
        value = (value * value) % RANDOM_MODULUS


def frictionlessTubeDistance(length, marbleCount, marbleIndex):
    compressedEastLimit = length - MARBLE_DIAMETER * (marbleCount - 1)
    baseExitDistances = []

    for compressedPosition, movingEast in generatedMarbleData(marbleCount):
        if movingEast:
            baseDistance = compressedEastLimit - compressedPosition
        else:
            baseDistance = (
                compressedPosition
                - WEST_CENTER_LIMIT
                + compressedEastLimit
                - WEST_CENTER_LIMIT
            )
        baseExitDistances.append(baseDistance)

    exitRank = marbleCount - marbleIndex + 1
    baseExitDistances.sort()
    return (
        baseExitDistances[exitRank - 1]
        + MARBLE_DIAMETER * (exitRank - 1)
    )


def runTests():
    assert frictionlessTubeDistance(5_000, 3, 2) == 5_519
    assert frictionlessTubeDistance(10_000, 11, 6) == 11_780
    assert frictionlessTubeDistance(100_000, 101, 51) == 114_101


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = frictionlessTubeDistance(1_000_000_000, 1_000_001, 500_001)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
