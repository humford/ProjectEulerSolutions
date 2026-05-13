import functools
import time


MODULUS = 10 ** 9
INITIAL_PATH_COUNTS = [1, 1, 1, 2, 6, 14, 28, 56]


def nextFrogPathCount(last1, last2, last3, last4, last5, last6, last7, last8):
    return 2 * last1 - last2 + 2 * last3 + last4 + last5 - last7 - last8


def frogPathCountsUpTo(limit):
    if limit <= 0:
        return [0]

    counts = [0] + INITIAL_PATH_COUNTS[:]
    if limit <= len(INITIAL_PATH_COUNTS):
        return counts[:limit + 1]

    for stones in range(len(INITIAL_PATH_COUNTS) + 1, limit + 1):
        counts.append(
            nextFrogPathCount(
                counts[stones - 1],
                counts[stones - 2],
                counts[stones - 3],
                counts[stones - 4],
                counts[stones - 5],
                counts[stones - 6],
                counts[stones - 7],
                counts[stones - 8],
            )
        )

    return counts


def buildCompanionMatrix(modulus):
    coefficients = [2, -1, 2, 1, 1, 0, -1, -1]
    matrix = [[0] * 8 for _ in range(8)]
    matrix[0] = [coefficient % modulus for coefficient in coefficients]
    for index in range(1, 8):
        matrix[index][index - 1] = 1
    return matrix


def matrixMultiply(left, right, modulus):
    result = [[0] * 8 for _ in range(8)]
    for rowIndex in range(8):
        row = left[rowIndex]
        for middle in range(8):
            value = row[middle]
            if not value:
                continue
            rightRow = right[middle]
            for column in range(8):
                result[rowIndex][column] = (
                    result[rowIndex][column] + value * rightRow[column]
                ) % modulus
    return result


def tensorFromVector(vector, modulus):
    tensor = [0] * 512
    reduced = [value % modulus for value in vector]

    for first in range(8):
        firstValue = reduced[first]
        for second in range(8):
            pairValue = firstValue * reduced[second] % modulus
            offset = first * 64 + second * 8
            for third in range(8):
                tensor[offset + third] = pairValue * reduced[third] % modulus

    return tensor


def transformTensor(matrix, tensor, modulus):
    firstPass = [0] * 512
    for second in range(8):
        for third in range(8):
            offset = second * 8 + third
            for first in range(8):
                row = matrix[first]
                total = 0
                for oldFirst in range(8):
                    total += row[oldFirst] * tensor[oldFirst * 64 + offset]
                firstPass[first * 64 + offset] = total % modulus

    secondPass = [0] * 512
    for first in range(8):
        firstOffset = first * 64
        for third in range(8):
            for second in range(8):
                row = matrix[second]
                total = 0
                for oldSecond in range(8):
                    total += row[oldSecond] * firstPass[firstOffset + oldSecond * 8 + third]
                secondPass[firstOffset + second * 8 + third] = total % modulus

    thirdPass = [0] * 512
    for first in range(8):
        firstOffset = first * 64
        for second in range(8):
            offset = firstOffset + second * 8
            for third in range(8):
                row = matrix[third]
                total = 0
                for oldThird in range(8):
                    total += row[oldThird] * secondPass[offset + oldThird]
                thirdPass[offset + third] = total % modulus

    return thirdPass


def sumCubesFromState(state, length, matrix, modulus):
    if length <= 0:
        return 0

    blockMatrices = []
    blockTensors = []
    powerMatrix = [row[:] for row in matrix]
    powerTensor = tensorFromVector(state, modulus)
    blockLength = 1

    while blockLength <= length:
        blockMatrices.append(powerMatrix)
        blockTensors.append(powerTensor)

        transformed = transformTensor(powerMatrix, powerTensor, modulus)
        powerTensor = [
            (powerTensor[index] + transformed[index]) % modulus
            for index in range(512)
        ]
        powerMatrix = matrixMultiply(powerMatrix, powerMatrix, modulus)
        blockLength <<= 1

    offsetMatrix = [[0] * 8 for _ in range(8)]
    for index in range(8):
        offsetMatrix[index][index] = 1

    accumulated = [0] * 512
    bit = 0
    remaining = length
    while remaining:
        if remaining & 1:
            contribution = transformTensor(offsetMatrix, blockTensors[bit], modulus)
            accumulated = [
                (accumulated[index] + contribution[index]) % modulus
                for index in range(512)
            ]
            offsetMatrix = matrixMultiply(offsetMatrix, blockMatrices[bit], modulus)

        remaining >>= 1
        bit += 1

    return accumulated[0]


def frogPathCubeSumMod(limit, modulus=MODULUS):
    if limit <= 0:
        return 0
    if limit <= 8:
        return sum(count ** 3 for count in INITIAL_PATH_COUNTS[:limit]) % modulus

    prefix = sum(count ** 3 for count in INITIAL_PATH_COUNTS[:7]) % modulus
    state = list(reversed(INITIAL_PATH_COUNTS))
    matrix = buildCompanionMatrix(modulus)
    return (prefix + sumCubesFromState(state, limit - 7, matrix, modulus)) % modulus


def frogPathCubeSumExact(limit):
    counts = frogPathCountsUpTo(limit)
    return sum(counts[index] ** 3 for index in range(1, limit + 1))


def frogPathCubeSum(limit):
    if limit <= 40:
        return frogPathCubeSumExact(limit)
    return frogPathCubeSumMod(limit)


def frogPaths(stones):
    return frogPathCountsUpTo(stones)[stones]


def bruteFrogPaths(stones):
    fullMask = (1 << stones) - 1

    @functools.lru_cache(None)
    def count(position, mask):
        if mask == fullMask:
            return 1 if position == stones - 1 else 0
        if position == stones - 1:
            return 0

        total = 0
        for nextPosition in range(max(0, position - 3), min(stones, position + 4)):
            if nextPosition != position and not mask & (1 << nextPosition):
                total += count(nextPosition, mask | (1 << nextPosition))
        return total

    return count(0, 1)


def runTests():
    for stones in range(1, 11):
        assert frogPaths(stones) == bruteFrogPaths(stones)

    assert frogPaths(6) == 14
    assert frogPaths(10) == 254
    assert frogPaths(40) == 1_439_682_432_976
    assert frogPathCubeSum(10) == 18_230_635
    assert frogPathCubeSum(20) == 104_207_881_192_114_219
    assert frogPathCubeSumMod(1_000) == 225_031_475
    assert frogPathCubeSumMod(1_000_000) == 363_486_179


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = frogPathCubeSumMod(10 ** 14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
