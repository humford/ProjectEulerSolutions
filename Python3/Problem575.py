import time
from fractions import Fraction


def exitCount(room, size):
    row = (room - 1) // size
    column = (room - 1) % size
    exits = 4

    if row == 0:
        exits -= 1
    if row == size - 1:
        exits -= 1
    if column == 0:
        exits -= 1
    if column == size - 1:
        exits -= 1

    return exits


def squareRoomProbabilityExact(size):
    if size == 1:
        return Fraction(1, 1)

    squareExitSum = sum(exitCount(square * square, size) for square in range(1, size + 1))
    dynamicStayWeight = squareExitSum + size
    totalExitWeight = 4 * size * (size - 1)
    totalDynamicStayWeight = totalExitWeight + size * size

    routeRelatedProbability = Fraction(dynamicStayWeight, totalDynamicStayWeight)
    fixedStayProbability = Fraction(squareExitSum, totalExitWeight)
    return (routeRelatedProbability + fixedStayProbability) / 2


def squareRoomProbability(size):
    return "{:.12f}".format(float(squareRoomProbabilityExact(size)))


def runTests():
    assert exitCount(1, 5) == 2
    assert exitCount(9, 5) == 4
    assert exitCount(16, 5) == 3
    assert squareRoomProbabilityExact(5) == Fraction(299, 1680)
    assert squareRoomProbability(5) == "0.177976190476"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squareRoomProbability(1_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
