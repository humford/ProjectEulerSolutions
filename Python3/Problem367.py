import itertools
import math
import time
from collections import Counter


SIZE = 11


def partitions(number, minimum=1):
    if number == 0:
        yield ()
        return

    for first in range(minimum, number + 1):
        for rest in partitions(number - first, first):
            yield (first,) + rest


def representativePermutation(partition):
    size = sum(partition)
    permutation = list(range(size))
    start = 0

    for length in partition:
        cycle = list(range(start, start + length))

        for index in range(length):
            permutation[cycle[index]] = cycle[(index + 1) % length]

        start += length

    return permutation


def cycleType(permutation):
    seen = [False] * len(permutation)
    lengths = []

    for start in range(len(permutation)):
        if seen[start]:
            continue

        current = start
        length = 0

        while not seen[current]:
            seen[current] = True
            length += 1
            current = permutation[current]

        lengths.append(length)

    return tuple(sorted(lengths))


def transitionCounts(partition):
    size = sum(partition)
    permutation = representativePermutation(partition)
    counts = Counter()

    for triple in itertools.combinations(range(size), 3):
        for ordering in itertools.permutations(triple):
            newPermutation = permutation[:]

            for destination, source in zip(triple, ordering):
                newPermutation[destination] = permutation[source]

            counts[cycleType(newPermutation)] += 1

    return counts, math.comb(size, 3) * 6


def classSize(partition):
    denominator = 1

    for length, count in Counter(partition).items():
        denominator *= (length**count) * math.factorial(count)

    return math.factorial(sum(partition)) // denominator


def expectedShuffleAverage(size=SIZE):
    allPartitions = list(partitions(size))
    identity = (1,) * size
    states = [partition for partition in allPartitions if partition != identity]
    index = {partition: i for i, partition in enumerate(states)}
    dimension = len(states)
    matrix = [[0.0] * dimension for _ in range(dimension)]
    rhs = [1.0] * dimension

    for partition in states:
        row = index[partition]
        matrix[row][row] = 1.0
        counts, denominator = transitionCounts(partition)

        for nextPartition, count in counts.items():
            if nextPartition != identity:
                matrix[row][index[nextPartition]] -= count / denominator

    for column in range(dimension):
        pivot = max(range(column, dimension), key=lambda row: abs(matrix[row][column]))
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        rhs[column], rhs[pivot] = rhs[pivot], rhs[column]
        pivotValue = matrix[column][column]

        for j in range(column, dimension):
            matrix[column][j] /= pivotValue

        rhs[column] /= pivotValue

        for row in range(dimension):
            if row == column:
                continue

            factor = matrix[row][column]

            if abs(factor) < 1e-15:
                continue

            for j in range(column, dimension):
                matrix[row][j] -= factor * matrix[column][j]

            rhs[row] -= factor * rhs[column]

    expected = {states[i]: rhs[i] for i in range(dimension)}
    expected[identity] = 0.0

    return (
        sum(classSize(partition) * expected[partition] for partition in allPartitions)
        / math.factorial(size)
    )


def runTests():
    assert round(expectedShuffleAverage(4), 10) == 27.5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = round(expectedShuffleAverage())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
