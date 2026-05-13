import time
from bisect import bisect_left
from functools import lru_cache


LIMIT = 200000

COMPLETE_LENGTHS = []
length = 1
while length < 400000:
    COMPLETE_LENGTHS.append(length)
    length = 2 * length + 1


@lru_cache(None)
def completeTreeCoefficients(length):
    if length <= 0:
        return 0, 0

    if length == 1:
        return 1, 0

    if length == 2:
        return 1, 1

    index = bisect_left(COMPLETE_LENGTHS, length)
    completeLeftLength = COMPLETE_LENGTHS[index - 1]
    pivotOffset = min(
        completeLeftLength, length - (completeLeftLength - 1) // 2
    )

    leftMultiplier, leftConstant = completeTreeCoefficients(pivotOffset - 1)
    rightMultiplier, rightConstant = completeTreeCoefficients(length - pivotOffset - 1)
    shiftedRightConstant = rightConstant + rightMultiplier * (pivotOffset + 1)

    if leftMultiplier > rightMultiplier:
        branchMultiplier, branchConstant = leftMultiplier, leftConstant
    elif rightMultiplier > leftMultiplier:
        branchMultiplier, branchConstant = rightMultiplier, shiftedRightConstant
    elif leftConstant >= shiftedRightConstant:
        branchMultiplier, branchConstant = leftMultiplier, leftConstant
    else:
        branchMultiplier, branchConstant = rightMultiplier, shiftedRightConstant

    return branchMultiplier + 1, pivotOffset + branchConstant


def completeTreeCost(low, high):
    multiplier, constant = completeTreeCoefficients(high - low)
    return multiplier * low + constant


def lowestCostSearchSum(limit=LIMIT):
    if limit <= 0:
        return 0

    costs = [0] * (limit + 1)
    seeds = {1: 0, 2: 1, 3: 2, 4: 4, 5: 6, 6: 8}

    for index, value in seeds.items():
        if index <= limit:
            costs[index] = value

    if limit <= 6:
        return sum(costs[1 : limit + 1])

    distance = 3
    distanceOffsets = [0]
    offset = 4

    while offset <= 131072:
        distanceOffsets.append(offset)
        offset *= 2

    offsetLimit = 2
    total = sum(costs[1:7])

    for size in range(7, limit + 1):
        if distance > 4**offsetLimit:
            offsetLimit += 1

        bestCost = None
        bestDistance = None

        for extraDistance in distanceOffsets[:offsetLimit]:
            guess = size - distance - extraDistance

            if not 0 < guess < size:
                continue

            left = costs[guess - 1]
            right = completeTreeCost(guess + 1, size)
            worst = max(left, right)
            candidate = guess + worst

            if bestCost is None or candidate < bestCost:
                bestCost = candidate
                bestDistance = distance + extraDistance

        costs[size] = bestCost
        distance = bestDistance
        total += bestCost

    return total


def runTests():
    def cost(index):
        return lowestCostSearchSum(index) - lowestCostSearchSum(index - 1)

    assert cost(1) == 0
    assert cost(2) == 1
    assert cost(3) == 2
    assert cost(8) == 12
    assert cost(100) == 400
    assert lowestCostSearchSum(100) == 17575


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lowestCostSearchSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
