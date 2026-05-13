import time


SEQUENCE_MODULUS = 998_388_889
TARGET_N = 10_000_000


def appendBlock(blocks, value):
    blocks.append([1, value, 0])

    while len(blocks) >= 2:
        left = blocks[-2]
        right = blocks[-1]
        if left[1] * right[0] <= right[1] * left[0]:
            break

        rightLength, rightSum, rightWeighted = blocks.pop()
        leftLength, leftSum, leftWeighted = blocks.pop()
        blocks.append([
            leftLength + rightLength,
            leftSum + rightSum,
            leftWeighted + rightWeighted + leftLength * rightSum,
        ])


def buildIncrementBlocks(n):
    value = 102_022_661
    firstA = value
    previousA = value

    value = value * value % SEQUENCE_MODULUS
    firstB = value
    previousB = value

    aBlocks = []
    bBlocks = []

    for _ in range(1, n):
        value = value * value % SEQUENCE_MODULUS
        currentA = value
        appendBlock(aBlocks, currentA - previousA)
        previousA = currentA

        value = value * value % SEQUENCE_MODULUS
        currentB = value
        appendBlock(bBlocks, currentB - previousB)
        previousB = currentB

    return firstA, firstB, aBlocks, bBlocks


def A(n):
    firstA, firstB, aBlocks, bBlocks = buildIncrementBlocks(n)
    total = (2 * n - 1) * (firstA + firstB)
    remainingCells = 2 * n - 2
    aIndex = 0
    bIndex = 0

    while aIndex < len(aBlocks) or bIndex < len(bBlocks):
        if bIndex == len(bBlocks) or (
            aIndex < len(aBlocks)
            and aBlocks[aIndex][1] * bBlocks[bIndex][0]
            <= bBlocks[bIndex][1] * aBlocks[aIndex][0]
        ):
            length, blockSum, weighted = aBlocks[aIndex]
            aIndex += 1
        else:
            length, blockSum, weighted = bBlocks[bIndex]
            bIndex += 1

        total += remainingCells * blockSum - weighted
        remainingCells -= length

    return total


def solve():
    return A(TARGET_N)


def runTests():
    assert A(1) == 966_774_091
    assert A(2) == 2_388_327_490
    assert A(10) == 13_389_278_727
    assert solve() == 9_986_212_680_734_636


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
