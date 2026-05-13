import time


MOD = 998_244_353
DISJOINT_BIT_MATRIX = ((1, 1), (1, 0))


class TensorTrain:
    def __init__(self, cores):
        self.cores = cores
        self.length = len(cores)


def allOnes(length):
    return TensorTrain([[[[1], [1]]] for _ in range(length)])


def indicatorLessEqual(bound, length):
    bits = [(bound >> (length - 1 - i)) & 1 for i in range(length)]
    cores = []

    if length == 1:
        bit = bits[0]
        transitions = (
            ((1, 0), (0, 1)) if bit == 0 else ((1, 0), (1, 0)),
            ((1, 0), (0, 0)) if bit == 0 else ((1, 0), (0, 1)),
        )
        core = [[[0], [0]]]
        for xBit, transition in enumerate(transitions):
            core[0][xBit][0] = (transition[1][0] + transition[1][1]) % MOD
        return TensorTrain([core])

    for index, bit in enumerate(bits):
        transitions = (
            ((1, 0), (0, 1)) if bit == 0 else ((1, 0), (1, 0)),
            ((1, 0), (0, 0)) if bit == 0 else ((1, 0), (0, 1)),
        )

        if index == 0:
            core = [[[0, 0], [0, 0]]]
            for xBit, transition in enumerate(transitions):
                core[0][xBit][0] = transition[1][0]
                core[0][xBit][1] = transition[1][1]
        elif index == length - 1:
            core = [[[0], [0]] for _ in range(2)]
            for previous in range(2):
                for xBit, transition in enumerate(transitions):
                    core[previous][xBit][0] = (
                        transition[previous][0] + transition[previous][1]
                    ) % MOD
        else:
            core = [[[0, 0], [0, 0]] for _ in range(2)]
            for previous in range(2):
                for xBit, transition in enumerate(transitions):
                    core[previous][xBit][0] = transition[previous][0]
                    core[previous][xBit][1] = transition[previous][1]
        cores.append(core)

    return TensorTrain(cores)


def scalarMultiply(tensor, coefficient):
    cores = [[[row[:] for row in slice_] for slice_ in core] for core in tensor.cores]
    for left in range(len(cores[0])):
        for bit in range(2):
            for right in range(len(cores[0][left][bit])):
                cores[0][left][bit][right] = cores[0][left][bit][right] * coefficient % MOD
    return TensorTrain(cores)


def addTensorTrains(left, right, rightCoefficient=1):
    assert left.length == right.length
    rightCoefficient %= MOD
    cores = []

    for index in range(left.length):
        A = left.cores[index]
        B = right.cores[index]
        leftRankA, rightRankA = len(A), len(A[0][0])
        leftRankB, rightRankB = len(B), len(B[0][0])

        if index == 0:
            core = [[[0] * (rightRankA + rightRankB) for _ in range(2)]]
            for bit in range(2):
                core[0][bit][:rightRankA] = A[0][bit][:]
                core[0][bit][rightRankA:] = [
                    rightCoefficient * value % MOD for value in B[0][bit]
                ]
        elif index == left.length - 1:
            core = [[[0], [0]] for _ in range(leftRankA + leftRankB)]
            for row in range(leftRankA):
                core[row][0][0] = A[row][0][0]
                core[row][1][0] = A[row][1][0]
            for row in range(leftRankB):
                core[leftRankA + row][0][0] = B[row][0][0]
                core[leftRankA + row][1][0] = B[row][1][0]
        else:
            core = [
                [[0] * (rightRankA + rightRankB) for _ in range(2)]
                for _ in range(leftRankA + leftRankB)
            ]
            for row in range(leftRankA):
                core[row][0][:rightRankA] = A[row][0][:]
                core[row][1][:rightRankA] = A[row][1][:]
            for row in range(leftRankB):
                core[leftRankA + row][0][rightRankA:] = B[row][0][:]
                core[leftRankA + row][1][rightRankA:] = B[row][1][:]
        cores.append(core)

    return TensorTrain(cores)


def hadamardProduct(left, right):
    assert left.length == right.length
    cores = []

    for index in range(left.length):
        A = left.cores[index]
        B = right.cores[index]
        leftRankA, rightRankA = len(A), len(A[0][0])
        leftRankB, rightRankB = len(B), len(B[0][0])
        core = [
            [[0] * (rightRankA * rightRankB) for _ in range(2)]
            for _ in range(leftRankA * leftRankB)
        ]

        for la in range(leftRankA):
            for lb in range(leftRankB):
                leftIndex = la * leftRankB + lb
                for bit in range(2):
                    for ra in range(rightRankA):
                        av = A[la][bit][ra]
                        if not av:
                            continue
                        base = ra * rightRankB
                        for rb in range(rightRankB):
                            core[leftIndex][bit][base + rb] = (
                                core[leftIndex][bit][base + rb] + av * B[lb][bit][rb]
                            ) % MOD
        cores.append(core)

    return TensorTrain(cores)


def applyLocalMatrix(tensor, matrix):
    m00, m01 = matrix[0]
    m10, m11 = matrix[1]
    cores = []

    for core in tensor.cores:
        leftRank = len(core)
        rightRank = len(core[0][0])
        newCore = [[[0] * rightRank for _ in range(2)] for _ in range(leftRank)]
        for left in range(leftRank):
            old0 = core[left][0]
            old1 = core[left][1]
            for right in range(rightRank):
                newCore[left][0][right] = (m00 * old0[right] + m01 * old1[right]) % MOD
                newCore[left][1][right] = (m10 * old0[right] + m11 * old1[right]) % MOD
        cores.append(newCore)

    return TensorTrain(cores)


def sumAll(tensor):
    vector = [1]
    for core in tensor.cores:
        newVector = [0] * len(core[0][0])
        for left, value in enumerate(vector):
            if not value:
                continue
            for right in range(len(newVector)):
                newVector[right] = (
                    newVector[right] + value * (core[left][0][right] + core[left][1][right])
                ) % MOD
        vector = newVector
    return vector[0] % MOD


def reducePivotColumns(rows):
    rowCount = len(rows)
    columnCount = len(rows[0]) if rowCount else 0
    pivots = []
    rank = 0

    for column in range(columnCount):
        pivot = None
        for row in range(rank, rowCount):
            if rows[row][column]:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != rank:
            rows[rank], rows[pivot] = rows[pivot], rows[rank]

        pivotRow = rows[rank]
        inverse = pow(pivotRow[column], MOD - 2, MOD)
        for j in range(column, columnCount):
            pivotRow[j] = pivotRow[j] * inverse % MOD

        for row in range(rank + 1, rowCount):
            factor = rows[row][column]
            if factor:
                for j in range(column, columnCount):
                    rows[row][j] = (rows[row][j] - factor * pivotRow[j]) % MOD

        pivots.append(column)
        rank += 1
        if rank == rowCount:
            break

    for pivotIndex in range(rank - 1, -1, -1):
        column = pivots[pivotIndex]
        pivotRow = rows[pivotIndex]
        for row in range(pivotIndex):
            factor = rows[row][column]
            if factor:
                for j in range(column, columnCount):
                    rows[row][j] = (rows[row][j] - factor * pivotRow[j]) % MOD

    return pivots, rank


def reduceLeft(tensor):
    cores = [core for core in tensor.cores]
    for index in range(len(cores) - 1):
        core = cores[index]
        leftRank = len(core)
        rightRank = len(core[0][0])
        rows = [None] * (2 * leftRank)
        for left in range(leftRank):
            rows[2 * left] = core[left][0][:]
            rows[2 * left + 1] = core[left][1][:]

        pivots, rank = reducePivotColumns(rows)
        if rank == rightRank:
            continue

        newCore = [[[0] * rank for _ in range(2)] for _ in range(leftRank)]
        for left in range(leftRank):
            for newColumn, oldColumn in enumerate(pivots):
                newCore[left][0][newColumn] = core[left][0][oldColumn]
                newCore[left][1][newColumn] = core[left][1][oldColumn]
        cores[index] = newCore

        nextCore = cores[index + 1]
        nextRightRank = len(nextCore[0][0])
        newNext = [[[0] * nextRightRank for _ in range(2)] for _ in range(rank)]
        pivotSet = set(pivots)

        for newColumn, oldColumn in enumerate(pivots):
            for bit in range(2):
                for right in range(nextRightRank):
                    newNext[newColumn][bit][right] = (
                        newNext[newColumn][bit][right] + nextCore[oldColumn][bit][right]
                    ) % MOD

        for oldColumn in range(rightRank):
            if oldColumn in pivotSet:
                continue
            for newColumn in range(rank):
                coefficient = rows[newColumn][oldColumn]
                if coefficient:
                    for bit in range(2):
                        for right in range(nextRightRank):
                            newNext[newColumn][bit][right] = (
                                newNext[newColumn][bit][right]
                                + coefficient * nextCore[oldColumn][bit][right]
                            ) % MOD

        cores[index + 1] = newNext

    return TensorTrain(cores)


def c(length, bound):
    bits = max(1, bound.bit_length())
    mask = indicatorLessEqual(bound, bits)
    dp = reduceLeft(mask)
    ones = allOnes(bits)

    for _ in range(length - 1):
        total = sumAll(dp)
        allTransitions = scalarMultiply(ones, total)
        disjointTransitions = applyLocalMatrix(dp, DISJOINT_BIT_MATRIX)
        nextDp = addTensorTrains(allTransitions, disjointTransitions, rightCoefficient=-1)
        nextDp = hadamardProduct(nextDp, mask)
        dp = reduceLeft(nextDp)

    return sumAll(dp)


def bruteC(length, bound):
    values = list(range(bound + 1))
    current = {value: 1 for value in values}
    for _ in range(length - 1):
        nextCounts = {value: 0 for value in values}
        for previous, count in current.items():
            for value in values:
                if previous & value:
                    nextCounts[value] += count
        current = nextCounts
    return sum(current.values())


def runTests():
    assert c(3, 4) == 18
    assert c(4, 5) == bruteC(4, 5) % MOD
    assert c(10, 6) == 2_496_120
    assert c(100, 200) == 268_159_379


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = c(123, 123_456_789)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
