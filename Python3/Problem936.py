from math import comb
import time


TARGET = 50


def multisetCount(typeCountsBySize, targetSize, targetCount):
    dp = [[0] * (targetCount + 1) for _ in range(targetSize + 1)]
    dp[0][0] = 1

    for size, typeCount in enumerate(typeCountsBySize):
        if size == 0 or typeCount == 0:
            continue

        nextDp = [row[:] for row in dp]
        maxMultiplicity = min(targetCount, targetSize // size)
        coefficients = [
            comb(typeCount + multiplicity - 1, multiplicity)
            for multiplicity in range(maxMultiplicity + 1)
        ]

        for usedSize in range(targetSize + 1):
            for usedCount in range(targetCount + 1):
                ways = dp[usedSize][usedCount]
                if ways == 0:
                    continue

                roomSize = targetSize - usedSize
                roomCount = targetCount - usedCount
                for multiplicity in range(1, min(roomCount, roomSize // size) + 1):
                    nextDp[usedSize + multiplicity * size][
                        usedCount + multiplicity
                    ] += ways * coefficients[multiplicity]

        dp = nextDp

    return dp[targetSize][targetCount]


def rootedBranchCounts(maxSize):
    # A branch root has a parent outside the branch.  Every vertex degree is
    # therefore one plus its number of children, so the peerless condition
    # inside a branch is that adjacent child counts differ.
    counts = [[0] * (maxSize + 1) for _ in range(maxSize + 1)]
    counts[1][0] = 1

    for size in range(2, maxSize + 1):
        totalsBySize = [sum(counts[branchSize]) for branchSize in range(maxSize + 1)]

        for childCount in range(1, size):
            allowedCounts = [0] * size
            for branchSize in range(1, size):
                allowedCounts[branchSize] = (
                    totalsBySize[branchSize] - counts[branchSize][childCount]
                )

            counts[size][childCount] = multisetCount(
                allowedCounts,
                size - 1,
                childCount,
            )

    return counts


def uniqueCentroidCount(size, branchCounts):
    total = 0
    maxBranchSize = (size - 1) // 2
    totalsBySize = [sum(counts) for counts in branchCounts]

    for degree in range(1, size):
        allowedCounts = [0] * size
        forbiddenChildCount = degree - 1

        for branchSize in range(1, maxBranchSize + 1):
            forbidden = (
                branchCounts[branchSize][forbiddenChildCount]
                if forbiddenChildCount < len(branchCounts[branchSize])
                else 0
            )
            allowedCounts[branchSize] = (
                totalsBySize[branchSize] - forbidden
            )

        total += multisetCount(allowedCounts, size - 1, degree)

    return total


def bicentroidCount(size, branchCounts):
    if size % 2 == 1:
        return 0

    half = size // 2
    total = sum(branchCounts[half])
    sameRootChildCount = sum(count * count for count in branchCounts[half])
    return (total * total - sameRootChildCount) // 2


def peerlessCounts(maxSize):
    branchCounts = rootedBranchCounts(maxSize // 2)
    counts = [0] * (maxSize + 1)

    if maxSize >= 1:
        counts[1] = 1

    for size in range(3, maxSize + 1):
        counts[size] = uniqueCentroidCount(size, branchCounts) + bicentroidCount(
            size,
            branchCounts,
        )

    return counts


def P(size):
    return peerlessCounts(size)[size]


def S(limit):
    counts = peerlessCounts(limit)
    return sum(counts[3 : limit + 1])


def solve():
    return S(TARGET)


def runTests():
    assert P(7) == 6
    assert S(10) == 74


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
