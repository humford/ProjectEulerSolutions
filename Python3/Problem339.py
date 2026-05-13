import time


LIMIT = 10_000


def expectedBlackSheep(count):
    midpointValues = [0.0] * (count + 1)
    centralProbability = 1.0

    for black in range(1, count + 1):
        ratio = 2.0 * centralProbability / (1.0 + centralProbability)
        totalSheep = 2 * black - 1
        midpointValues[black] = midpointValues[black - 1] + (
            totalSheep - midpointValues[black - 1]
        ) * ratio
        centralProbability *= (2.0 * black - 1.0) / (2.0 * black)

    oddCentralProbability = 0.5
    for index in range(1, count):
        oddCentralProbability *= (2.0 * index + 1.0) / (2.0 * index + 2.0)

    totalSheep = 2 * count
    nextMidpointValue = midpointValues[count] + (
        totalSheep - midpointValues[count]
    ) * (2.0 * oddCentralProbability)

    return 0.5 * (midpointValues[count - 1] + nextMidpointValue)


def runTests():
    assert abs(expectedBlackSheep(1) - 1.0) < 1e-12
    assert abs(expectedBlackSheep(2) - 55.0 / 24.0) < 1e-12
    assert abs(expectedBlackSheep(3) - 1981.0 / 528.0) < 1e-12
    assert round(expectedBlackSheep(5), 6) == 6.871346


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.6f}".format(expectedBlackSheep(LIMIT))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
