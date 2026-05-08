import time
from pathlib import Path


def readSets():
    path = Path(__file__).resolve().parents[1] / "Files" / "p105_sets.txt"
    return [
        [int(value) for value in line.split(",")]
        for line in path.read_text().strip().splitlines()
    ]


def hasIncreasingSubsetSums(values):
    values = sorted(values)
    for size in range(1, len(values) // 2 + 1):
        if sum(values[: size + 1]) <= sum(values[-size:]):
            return False
    return True


def hasUniqueSubsetSums(values):
    sums = set()

    for mask in range(1, 1 << len(values)):
        total = sum(values[index] for index in range(len(values)) if mask & (1 << index))
        if total in sums:
            return False
        sums.add(total)

    return True


def isSpecialSumSet(values):
    return hasIncreasingSubsetSums(values) and hasUniqueSubsetSums(values)


def specialSetSum(sets):
    return sum(sum(values) for values in sets if isSpecialSumSet(values))


def runTests():
    assert not isSpecialSumSet([81, 88, 75, 42, 87, 84, 86, 65])
    assert isSpecialSumSet([157, 150, 164, 119, 79, 159, 161, 139, 158])


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = specialSetSum(readSets())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
