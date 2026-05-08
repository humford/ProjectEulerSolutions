import itertools
import time


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


def optimumSpecialSumSet():
    seed = [20, 31, 38, 39, 40, 42, 45]
    best = seed
    best_sum = sum(seed)

    ranges = [range(value - 3, value + 4) for value in seed]
    for candidate in itertools.product(*ranges):
        if sorted(candidate) != list(candidate) or len(set(candidate)) != len(candidate):
            continue
        if sum(candidate) >= best_sum:
            continue
        if isSpecialSumSet(candidate):
            best = list(candidate)
            best_sum = sum(candidate)

    return best


def setString(values):
    return "".join(str(value) for value in values)


def runTests():
    assert isSpecialSumSet([3, 5, 6, 7])
    assert not isSpecialSumSet([1, 2, 3])


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = setString(optimumSpecialSumSet())
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
