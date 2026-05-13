import math
import time


def totientsUpTo(limit):
    totients = list(range(limit + 1))
    for value in range(2, limit + 1):
        if totients[value] == value:
            for multiple in range(value, limit + 1, value):
                totients[multiple] -= totients[multiple] // value
    return totients


def hasCoprimeInInterval(number, low, high):
    for value in range(low, high + 1):
        if math.gcd(value, number) == 1:
            return True
    return False


def boundaryVectorCount(totalStep, remainingBudget, totient):
    pairedVectors = totient // 2
    fullPairs = min(pairedVectors, remainingBudget // totalStep)
    remainingAfterPairs = remainingBudget - fullPairs * totalStep

    extraVector = 0
    if fullPairs < pairedVectors and 2 * remainingAfterPairs >= totalStep:
        low = max(1, totalStep - remainingAfterPairs)
        high = min(totalStep - 1, remainingAfterPairs)
        if hasCoprimeInInterval(totalStep, low, high):
            extraVector = 1

    return 2 * fullPairs + extraVector


def convexPathMaxPoints(n):
    limit = 1_000
    while True:
        totients = totientsUpTo(limit)
        coordinateSum = 0
        pointCount = 1
        totalStep = 1

        while (
            totalStep + 1 <= limit
            and coordinateSum
            + (totalStep + 1) * totients[totalStep + 1] // 2
            <= n
        ):
            totalStep += 1
            coordinateSum += totalStep * totients[totalStep] // 2
            pointCount += totients[totalStep]

        if totalStep + 1 <= limit:
            break

        limit *= 2

    boundaryStep = totalStep + 1
    remainingBudget = n - coordinateSum
    return pointCount + boundaryVectorCount(
        boundaryStep,
        remainingBudget,
        totients[boundaryStep],
    )


def runTests():
    assert convexPathMaxPoints(1) == 2
    assert convexPathMaxPoints(3) == 3
    assert convexPathMaxPoints(9) == 6
    assert convexPathMaxPoints(11) == 7
    assert convexPathMaxPoints(100) == 30
    assert convexPathMaxPoints(50_000) == 1_898


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = convexPathMaxPoints(10 ** 18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
