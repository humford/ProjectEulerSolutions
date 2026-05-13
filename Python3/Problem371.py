import time


PAIR_COUNT = 499
NUMBER_COUNT = 1000


def expectedPlates():
    without500 = [0.0] * (PAIR_COUNT + 1)
    with500 = [0.0] * (PAIR_COUNT + 1)

    for activePairs in range(PAIR_COUNT, -1, -1):
        noChange = (1 + activePairs) / NUMBER_COUNT
        newPair = 2 * (PAIR_COUNT - activePairs) / NUMBER_COUNT

        nextWith500 = with500[activePairs + 1] if activePairs < PAIR_COUNT else 0.0
        with500[activePairs] = (1.0 + newPair * nextWith500) / (1.0 - noChange)

        nextWithout500 = without500[activePairs + 1] if activePairs < PAIR_COUNT else 0.0
        without500[activePairs] = (
            1.0 + newPair * nextWithout500 + with500[activePairs] / NUMBER_COUNT
        ) / (1.0 - noChange)

    return without500[0]


def runTests():
    assert round(expectedPlates(), 8) == 40.66368097


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.8f}".format(expectedPlates())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
