import functools
import math
import time

import numpy as np


FERMAT_POWERS = (1, 2, 4, 16, 256, 65536)


def triangularLengths(limit):
    lengths = []
    index = 1
    while True:
        value = index * (index + 1) // 2
        if value > limit:
            break
        lengths.append(value)
        index += 1
    return np.array(lengths, dtype=np.int64)


def squareLengths(limit):
    return np.array(
        [index * index for index in range(1, math.isqrt(limit) + 1)],
        dtype=np.int64,
    )


@functools.lru_cache(None)
def nimberMultiply(a, b):
    if a < b:
        a, b = b, a
    if a == 0 or b == 0:
        return 0
    if a == 1:
        return b
    if b == 1:
        return a

    base = 1
    for fermatPower in FERMAT_POWERS:
        if fermatPower <= a:
            base = fermatPower
        else:
            break

    a1, a0 = divmod(a, base)
    b1, b0 = divmod(b, base)
    low = nimberMultiply(a0, b0)
    middle = nimberMultiply(a0, b1) ^ nimberMultiply(a1, b0)
    high = nimberMultiply(a1, b1)
    shift = base.bit_length() - 1
    return low ^ ((middle ^ high) << shift) ^ nimberMultiply(high, base >> 1)


def nimberPower(base, exponent):
    result = 1
    current = base
    while exponent:
        if exponent & 1:
            result = nimberMultiply(result, current)
        exponent >>= 1
        if exponent:
            current = nimberMultiply(current, current)
    return result


def computeSequence(limit, lengths, valueLimit):
    prefix = np.zeros(limit + 1, dtype=np.int32)
    counts = np.zeros(valueLimit, dtype=np.int64)
    present = np.zeros(valueLimit, dtype=np.int32)
    stamp = 1

    for end in range(1, limit + 1):
        count = np.searchsorted(lengths, end, side="right")
        values = np.bitwise_xor(int(prefix[end - 1]), prefix[end - lengths[:count]])
        if values.size and int(values.max()) >= valueLimit:
            return None, None, True

        present[values] = stamp
        grundy = 0
        while grundy < valueLimit and present[grundy] == stamp:
            grundy += 1
        if grundy == valueLimit:
            return None, None, True

        segmentValues = np.bitwise_xor(values, grundy)
        counts += np.bincount(segmentValues, minlength=valueLimit)[:valueLimit]
        prefix[end] = int(prefix[end - 1]) ^ grundy
        stamp += 1

    return int(prefix[limit]), counts, False


def rowAndColumnSequences(size):
    rows = triangularLengths(size)
    columns = squareLengths(size)
    valueLimit = 512

    while True:
        rowXor, rowCounts, rowOverflow = computeSequence(size, rows, valueLimit)
        colXor, colCounts, colOverflow = computeSequence(size, columns, valueLimit)
        if not rowOverflow and not colOverflow:
            return rowXor, rowCounts, colXor, colCounts
        valueLimit *= 2


def winningMoveCount(size):
    rowXor, rowCounts, colXor, colCounts = rowAndColumnSequences(size)
    totalXor = nimberMultiply(rowXor, colXor)
    rowTotal = int(rowCounts.sum())
    colTotal = int(colCounts.sum())

    if totalXor == 0:
        return int(rowCounts[0]) * colTotal + int(colCounts[0]) * rowTotal - int(rowCounts[0]) * int(colCounts[0])

    nonzeroRows = np.nonzero(rowCounts)[0]
    nonzeroCombined = np.nonzero((rowCounts != 0) | (colCounts != 0))[0]
    maxValue = totalXor
    if nonzeroCombined.size:
        maxValue = max(maxValue, int(nonzeroCombined[-1]))

    fieldSize = 2
    while fieldSize <= maxValue:
        fieldSize *= fieldSize

    inverseExponent = fieldSize - 2
    inverses = {1: 1}
    answer = 0
    for rowValue in nonzeroRows:
        rowValue = int(rowValue)
        if rowValue == 0:
            continue
        inverse = inverses.get(rowValue)
        if inverse is None:
            inverse = nimberPower(rowValue, inverseExponent)
            inverses[rowValue] = inverse
        colValue = nimberMultiply(inverse, totalXor)
        if colValue < len(colCounts):
            answer += int(rowCounts[rowValue]) * int(colCounts[colValue])

    return answer


def runTests():
    assert winningMoveCount(1) == 1
    assert winningMoveCount(2) == 0
    assert winningMoveCount(5) == 8
    assert winningMoveCount(10**2) == 31395


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningMoveCount(10**6)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
