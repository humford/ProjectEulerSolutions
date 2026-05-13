import time
from pathlib import Path


MOD = 1_005_075_251
INPUT_FILE = Path("Files/p828_number_challenges.txt")


def parseChallenges(path=INPUT_FILE):
    challenges = []
    for line in path.read_text().splitlines():
        targetText, numbersText = line.split(":")
        numbers = [int(value) for value in numbersText.split(",")]
        challenges.append((int(targetText), numbers))
    return challenges


def combineValues(leftValues, rightValues):
    result = set()

    for left in leftValues:
        for right in rightValues:
            result.add(left + right)
            result.add(left * right)
            if left > right:
                result.add(left - right)
            elif right > left:
                result.add(right - left)
            if right and left % right == 0:
                result.add(left // right)
            if left and right % left == 0:
                result.add(right // left)

    return result


def reachableValuesByMask(numbers):
    count = len(numbers)
    totalMasks = 1 << count
    values = [set() for _ in range(totalMasks)]

    for i, value in enumerate(numbers):
        values[1 << i].add(value)

    for mask in range(1, totalMasks):
        if mask & (mask - 1) == 0:
            continue

        submask = (mask - 1) & mask
        while submask:
            other = mask ^ submask
            if submask < other:
                values[mask].update(combineValues(values[submask], values[other]))
            submask = (submask - 1) & mask

    return values


def subsetSums(numbers):
    sums = [0] * (1 << len(numbers))
    for mask in range(1, len(sums)):
        bit = mask & -mask
        index = bit.bit_length() - 1
        sums[mask] = sums[mask ^ bit] + numbers[index]
    return sums


def minScore(target, numbers):
    values = reachableValuesByMask(numbers)
    sums = subsetSums(numbers)
    best = None

    for mask in range(1, len(values)):
        if target in values[mask]:
            score = sums[mask]
            if best is None or score < best:
                best = score

    return best if best is not None else 0


def solve(challenges=None):
    if challenges is None:
        challenges = parseChallenges()

    total = 0
    power = 1
    for target, numbers in challenges:
        power = power * 3 % MOD
        total = (total + power * minScore(target, numbers)) % MOD

    return total


def runTests():
    assert minScore(211, [2, 3, 4, 6, 7, 25]) == 40
    firstTarget, firstNumbers = parseChallenges()[0]
    assert firstTarget == 211
    assert firstNumbers == [2, 3, 4, 6, 7, 25]
    assert minScore(firstTarget, firstNumbers) == 40


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
