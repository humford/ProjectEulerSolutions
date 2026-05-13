import time


MOD = 1_000_000_007


def recurrenceValue(n):
    if n == 1:
        return 1
    half = n // 2
    previous = recurrenceValue(half)
    if n % 2 == 0:
        return 2 * previous
    return n + 2 * previous + previous // half


def zeroMatrix():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def addMatrices(left, right):
    result = zeroMatrix()
    for popcountPower in range(3):
        for degree in range(3):
            result[popcountPower][degree] = (
                left[popcountPower][degree] + right[popcountPower][degree]
            ) % MOD
    return result


def shiftRange(matrix, powerOfTwo):
    p = powerOfTwo % MOD
    p2 = p * p % MOD
    twoP = 2 * p % MOD

    shiftedByDegree = zeroMatrix()
    for popcountPower in range(3):
        s0 = matrix[popcountPower][0]
        s1 = matrix[popcountPower][1]
        s2 = matrix[popcountPower][2]
        shiftedByDegree[popcountPower][0] = s0
        shiftedByDegree[popcountPower][1] = (p * s0 + s1) % MOD
        shiftedByDegree[popcountPower][2] = (p2 * s0 + twoP * s1 + s2) % MOD

    result = zeroMatrix()
    coefficients = ((1, 0, 0), (1, 1, 0), (1, 2, 1))
    for newPower, row in enumerate(coefficients):
        for degree in range(3):
            result[newPower][degree] = (
                row[0] * shiftedByDegree[0][degree]
                + row[1] * shiftedByDegree[1][degree]
                + row[2] * shiftedByDegree[2][degree]
            ) % MOD
    return result


def precomputeFullBlocks(maxBits):
    full = [zeroMatrix() for _ in range(maxBits + 1)]
    full[0][0][0] = 1
    for bits in range(1, maxBits + 1):
        powerOfTwo = 1 << (bits - 1)
        full[bits] = addMatrices(full[bits - 1], shiftRange(full[bits - 1], powerOfTwo))
    return full


def aggregateUpTo(n, fullBlocks):
    if n < 0:
        return zeroMatrix()
    if n == 0:
        return fullBlocks[0]

    bits = n.bit_length() - 1
    powerOfTwo = 1 << bits
    if n == powerOfTwo - 1:
        return fullBlocks[bits]

    return addMatrices(
        fullBlocks[bits],
        shiftRange(aggregateUpTo(n - powerOfTwo, fullBlocks), powerOfTwo),
    )


def squaredRecurrenceSum(n):
    fullBlocks = precomputeFullBlocks(n.bit_length())
    return aggregateUpTo(n, fullBlocks)[2][2] % MOD


def slowSquaredRecurrenceSum(limit):
    return sum(recurrenceValue(n) ** 2 for n in range(1, limit + 1)) % MOD


def runTests():
    for n in range(1, 100):
        assert recurrenceValue(n) == n * n.bit_count()

    assert squaredRecurrenceSum(10) == 1_530
    assert squaredRecurrenceSum(10 ** 2) == 4_798_445
    assert squaredRecurrenceSum(1_000) == slowSquaredRecurrenceSum(1_000)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squaredRecurrenceSum(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
