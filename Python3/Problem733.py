import time
from array import array


SEQUENCE_MODULUS = 10_000_019
BASE = 153
MODULUS = 1_000_000_007
SHIFT = 32
MASK = (1 << SHIFT) - 1


def sequenceValues(count):
    values = array("I")
    value = BASE % SEQUENCE_MODULUS
    for _ in range(count):
        values.append(value)
        value = value * BASE % SEQUENCE_MODULUS
    return values


def compressedRanks(values):
    indexes = list(range(len(values)))
    indexes.sort(key=values.__getitem__)

    ranks = array("I", [0]) * len(values)
    rank = 0
    previous = None
    for index in indexes:
        value = values[index]
        if value != previous:
            rank += 1
            previous = value
        ranks[index] = rank

    return ranks, rank


def fenwickPrefixSum(tree, index):
    count = 0
    valueSum = 0
    while index:
        packed = tree[index]
        count += packed >> SHIFT
        valueSum += packed & MASK
        index -= index & -index
    return count % MODULUS, valueSum % MODULUS


def fenwickAdd(tree, size, index, countDelta, sumDelta):
    countDelta %= MODULUS
    sumDelta %= MODULUS

    while index <= size:
        packed = tree[index]
        count = (packed >> SHIFT) + countDelta
        if count >= MODULUS:
            count -= MODULUS
        valueSum = (packed & MASK) + sumDelta
        if valueSum >= MODULUS:
            valueSum -= MODULUS
        tree[index] = (count << SHIFT) | valueSum
        index += index & -index


def ascendingSubsequenceSum(count):
    values = sequenceValues(count)
    ranks, rankCount = compressedRanks(values)

    length1 = array("Q", [0]) * (rankCount + 1)
    length2 = array("Q", [0]) * (rankCount + 1)
    length3 = array("Q", [0]) * (rankCount + 1)

    total = 0
    for value, rank in zip(values, ranks):
        value = int(value)
        rank = int(rank)
        previousRank = rank - 1

        count3, sum3 = fenwickPrefixSum(length3, previousRank)
        total = (total + sum3 + count3 * value) % MODULUS

        count2, sum2 = fenwickPrefixSum(length2, previousRank)
        fenwickAdd(length3, rankCount, rank, count2, sum2 + count2 * value)

        count1, sum1 = fenwickPrefixSum(length1, previousRank)
        fenwickAdd(length2, rankCount, rank, count1, sum1 + count1 * value)

        fenwickAdd(length1, rankCount, rank, 1, value)

    return total


def ascendingSubsequenceSumExact(count):
    values = list(sequenceValues(count))
    ranks, rankCount = compressedRanks(array("I", values))

    def add(tree, index, delta):
        while index <= rankCount:
            tree[index] += delta
            index += index & -index

    def prefix(tree, index):
        total = 0
        while index:
            total += tree[index]
            index -= index & -index
        return total

    count1 = [0] * (rankCount + 1)
    sum1 = [0] * (rankCount + 1)
    count2 = [0] * (rankCount + 1)
    sum2 = [0] * (rankCount + 1)
    count3 = [0] * (rankCount + 1)
    sum3 = [0] * (rankCount + 1)

    total = 0
    for value, rank in zip(values, ranks):
        previousRank = rank - 1

        c3 = prefix(count3, previousRank)
        s3 = prefix(sum3, previousRank)
        total += s3 + c3 * value

        c2 = prefix(count2, previousRank)
        s2 = prefix(sum2, previousRank)
        add(count3, rank, c2)
        add(sum3, rank, s2 + c2 * value)

        c1 = prefix(count1, previousRank)
        s1 = prefix(sum1, previousRank)
        add(count2, rank, c1)
        add(sum2, rank, s1 + c1 * value)

        add(count1, rank, 1)
        add(sum1, rank, value)

    return total


def runTests():
    assert list(sequenceValues(6)) == [153, 23_409, 3_581_577, 7_980_255, 976_697, 9_434_375]
    assert ascendingSubsequenceSumExact(6) == 94_513_710
    assert ascendingSubsequenceSumExact(100) == 4_465_488_724_217


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = ascendingSubsequenceSum(10**6)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
