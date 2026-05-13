from collections import Counter
import math
import time


MODULUS = 1_001_001_011


def integerPartitions(total, minimumPart=1):
    if total == 0:
        yield []
        return

    for first in range(minimumPart, total + 1):
        for rest in integerPartitions(total - first, first):
            yield [first] + rest


def cycleTypeInfos(size):
    factorial = math.factorial(size)
    infos = []
    for parts in integerPartitions(size):
        counts = Counter(parts)
        centralizerSize = 1
        for cycleLength, count in counts.items():
            centralizerSize *= cycleLength ** count * math.factorial(count)
        infos.append((parts, factorial // centralizerSize))
    return infos


def binaryRank(rows):
    basis = {}
    rank = 0
    for row in rows:
        value = row
        while value:
            bit = value.bit_length() - 1
            if bit in basis:
                value ^= basis[bit]
            else:
                basis[bit] = value
                rank += 1
                break
    return rank


def parityConstraintRank(rowCycles, columnCycles):
    columnOffset = len(rowCycles)
    rows = []
    for rowIndex, rowLength in enumerate(rowCycles):
        for columnIndex, columnLength in enumerate(columnCycles):
            common = math.gcd(rowLength, columnLength)
            mask = 0
            if (columnLength // common) % 2 == 1:
                mask ^= 1 << rowIndex
            if (rowLength // common) % 2 == 1:
                mask ^= 1 << (columnOffset + columnIndex)
            if mask:
                rows.append(mask)
    return binaryRank(rows)


def burnsideContribution(rowCycles, rowPermutationCount, columnCycles, columnPermutationCount, size):
    cellOrbitCount = sum(math.gcd(rowLength, columnLength) for rowLength in rowCycles for columnLength in columnCycles)
    rank = parityConstraintRank(rowCycles, columnCycles)
    fixedMatrixSum = 1 << (2 * size + cellOrbitCount - rank)
    return rowPermutationCount * columnPermutationCount * fixedMatrixSum


def binaryMatrixClassCount(size):
    cycleTypes = cycleTypeInfos(size)
    total = 0
    for rowCycles, rowPermutationCount in cycleTypes:
        for columnCycles, columnPermutationCount in cycleTypes:
            total += burnsideContribution(
                rowCycles,
                rowPermutationCount,
                columnCycles,
                columnPermutationCount,
                size,
            )

    groupSize = (1 << (2 * size)) * math.factorial(size) ** 2
    assert total % groupSize == 0
    return (total // groupSize) % MODULUS


def runTests():
    assert binaryMatrixClassCount(3) == 3
    assert binaryMatrixClassCount(5) == 39
    assert binaryMatrixClassCount(8) == 656_108


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = binaryMatrixClassCount(20)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
