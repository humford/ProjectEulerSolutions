import math
import time


MODULUS = 1_000_000_007


def trollAttributeSeed(index):
    return (pow(5, index, MODULUS) % 101) + 50


def generateTrolls(trollCount):
    value = 1
    attributes = []
    for _ in range(3 * trollCount):
        attributes.append((value % 101) + 50)
        value = value * 5 % MODULUS

    trolls = []
    for index in range(trollCount):
        trolls.append(
            (
                attributes[3 * index],
                attributes[3 * index + 1],
                attributes[3 * index + 2],
            )
        )
    return trolls


def ceilDivSqrt2(value):
    return math.isqrt((value * value - 1) // 2) + 1


def escapingTrollIq(trollCount):
    trolls = generateTrolls(trollCount)
    totalHeight = sum(height for height, _, _ in trolls)
    depthCeiling = ceilDivSqrt2(totalHeight)
    deadlineBase = totalHeight - depthCeiling

    jobs = []
    maxDeadline = 0
    for height, armLength, iq in trolls:
        deadline = deadlineBase + armLength + height
        if height <= deadline:
            jobs.append((deadline, height, iq))
            if deadline > maxDeadline:
                maxDeadline = deadline

    jobs.sort()
    bestIqAtHeight = [-1] * (maxDeadline + 1)
    bestIqAtHeight[0] = 0

    for deadline, height, iq in jobs:
        for usedHeight in range(deadline, height - 1, -1):
            previous = bestIqAtHeight[usedHeight - height]
            if previous != -1:
                candidate = previous + iq
                if candidate > bestIqAtHeight[usedHeight]:
                    bestIqAtHeight[usedHeight] = candidate

    return max(bestIqAtHeight)


def runTests():
    assert trollAttributeSeed(0) == 51
    assert trollAttributeSeed(1) == 55
    assert trollAttributeSeed(2) == 75
    assert escapingTrollIq(5) == 401
    assert escapingTrollIq(15) == 941


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = escapingTrollIq(1_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
