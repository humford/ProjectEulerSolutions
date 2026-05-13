import math
import time


def unsignedStirlingFirstKind(size):
    counts = [[0] * (size + 1) for _ in range(size + 1)]
    counts[0][0] = 1
    for n in range(1, size + 1):
        for cycles in range(1, n + 1):
            counts[n][cycles] = counts[n - 1][cycles - 1] + (n - 1) * counts[n - 1][cycles]
    return counts[size]


def nonzeroTwistSums(maxLength):
    counts = [[0, 0, 0] for _ in range(maxLength + 1)]
    counts[0][0] = 1
    for length in range(maxLength):
        for residue in range(3):
            counts[length + 1][(residue + 1) % 3] += counts[length][residue]
            counts[length + 1][(residue + 2) % 3] += counts[length][residue]
    return [counts[length][0] for length in range(maxLength + 1)]


def rubikColourings(colours):
    cornerPermutationCounts = unsignedStirlingFirstKind(8)
    nonzeroSumCounts = nonzeroTwistSums(8)

    total = 0
    for cornerCycles in range(1, 9):
        twistAssignmentsPerCycleSum = 3 ** (8 - cornerCycles)
        cycleContribution = 0

        for zeroSumCycles in range(cornerCycles + 1):
            nonzeroCycles = cornerCycles - zeroSumCycles
            twistPatterns = math.comb(cornerCycles, zeroSumCycles) * nonzeroSumCounts[nonzeroCycles]
            faceletCycles = cornerCycles + 2 * zeroSumCycles
            cycleContribution += twistPatterns * (colours**faceletCycles)

        total += cornerPermutationCounts[cornerCycles] * twistAssignmentsPerCycleSum * cycleContribution

    groupSize = math.factorial(8) * (3**7)
    assert total % groupSize == 0
    return total // groupSize


def runTests():
    assert rubikColourings(2) == 183


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rubikColourings(10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
