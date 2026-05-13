import time


TARGET = "NOWPICKBELFRYMATHS"


def encodePermutation(word):
    letters = sorted(word)
    ranks = {letter: index + 1 for index, letter in enumerate(letters)}
    return [ranks[letter] for letter in word]


def johnsonTrotterRank(permutation):
    removals = []
    remaining = permutation[:]

    while len(remaining) > 1:
        size = len(remaining)
        largest = size
        position = remaining.index(largest)
        remaining.pop(position)
        removals.append((size, position))

    rank = 0
    for size, position in reversed(removals):
        offset = size - 1 - position if rank % 2 == 0 else position
        rank = rank * size + offset

    return rank


def johnsonTrotterRankRecursive(permutation):
    if len(permutation) <= 1:
        return 0

    size = len(permutation)
    largest = size
    position = permutation.index(largest)
    reduced = [value for value in permutation if value != largest]
    reducedRank = johnsonTrotterRankRecursive(reduced)
    offset = size - 1 - position if reducedRank % 2 == 0 else position
    return reducedRank * size + offset


def runTests():
    assert johnsonTrotterRankRecursive(encodePermutation("CBA")) == 3
    assert johnsonTrotterRankRecursive(encodePermutation("BELFRY")) == 59
    assert johnsonTrotterRank(encodePermutation("CBA")) == 3
    assert johnsonTrotterRank(encodePermutation("BELFRY")) == 59


def solve():
    return johnsonTrotterRank(encodePermutation(TARGET))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
