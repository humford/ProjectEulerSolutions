import time


LIMIT = 10**18
MODULUS = 10**9
BASE_LENGTH = 9
MATRIX_SIZE = 15


def sequence(length):
    values = [0, 1, 2, 3]

    while len(values) <= length:
        values.append(values[-1] + values[-3])

    return values[: length + 1]


def subsetCountAtMost(values, limit):
    sums = {0: 1}

    for value in values:
        for total, count in list(sums.items()):
            nextTotal = total + value

            if nextTotal <= limit:
                sums[nextTotal] = sums.get(nextTotal, 0) + count

    return sum(sums.values())


def polygonSubsetCountModerate(length):
    values = sequence(length)[1:]
    badSubsets = 1
    sums = {0: 1}

    for value in values:
        badSubsets += sum(count for total, count in sums.items() if total <= value)

        for total, count in list(sums.items()):
            sums[total + value] = sums.get(total + value, 0) + count

    return 2**length - badSubsets


def initialState():
    values = sequence(BASE_LENGTH)
    thresholdCounts = {
        length: subsetCountAtMost(values[1:length], values[length])
        for length in range(1, BASE_LENGTH + 1)
    }
    auxiliaryCounts = {
        length: subsetCountAtMost(
            values[1 : length - 2], values[length - 3] + values[length - 4]
        )
        for length in range(7, BASE_LENGTH + 1)
    }
    badSubsets = 1 + sum(thresholdCounts.values())

    return [
        thresholdCounts[9],
        thresholdCounts[8],
        thresholdCounts[7],
        thresholdCounts[6],
        auxiliaryCounts[9],
        auxiliaryCounts[8],
        auxiliaryCounts[7],
        2**9,
        2**8,
        2**7,
        2**6,
        2**5,
        2**4,
        badSubsets,
        1,
    ]


def transitionMatrix():
    matrix = [[0] * MATRIX_SIZE for _ in range(MATRIX_SIZE)]

    for column, coefficient in [
        (2, 1),
        (3, 1),
        (6, 1),
        (9, 1),
        (11, 1),
        (12, 1),
        (14, 2),
    ]:
        matrix[0][column] = coefficient

    matrix[1][0] = 1
    matrix[2][1] = 1
    matrix[3][2] = 1

    for column, coefficient in [(3, 1), (6, 1), (11, 1), (12, 1), (14, 1)]:
        matrix[4][column] = coefficient

    matrix[5][4] = 1
    matrix[6][5] = 1

    matrix[7][7] = 2
    matrix[8][7] = 1
    matrix[9][8] = 1
    matrix[10][9] = 1
    matrix[11][10] = 1
    matrix[12][11] = 1

    for column, coefficient in [
        (2, 1),
        (3, 1),
        (6, 1),
        (9, 1),
        (11, 1),
        (12, 1),
        (13, 1),
        (14, 2),
    ]:
        matrix[13][column] = coefficient

    matrix[14][14] = 1

    return matrix


def multiplyMatrices(left, right):
    product = [[0] * MATRIX_SIZE for _ in range(MATRIX_SIZE)]

    for row in range(MATRIX_SIZE):
        for middle in range(MATRIX_SIZE):
            if left[row][middle] == 0:
                continue

            leftValue = left[row][middle]

            for column in range(MATRIX_SIZE):
                product[row][column] = (
                    product[row][column] + leftValue * right[middle][column]
                ) % MODULUS

    return product


def multiplyMatrixVector(matrix, vector):
    product = [0] * MATRIX_SIZE

    for row in range(MATRIX_SIZE):
        total = 0

        for column in range(MATRIX_SIZE):
            total += matrix[row][column] * vector[column]

        product[row] = total % MODULUS

    return product


def polygonSubsetCount(length=LIMIT):
    state = initialState()

    if length <= BASE_LENGTH:
        return polygonSubsetCountModerate(length) % MODULUS

    matrix = transitionMatrix()
    exponent = length - BASE_LENGTH
    state = [value % MODULUS for value in state]

    while exponent > 0:
        if exponent % 2 == 1:
            state = multiplyMatrixVector(matrix, state)

        matrix = multiplyMatrices(matrix, matrix)
        exponent //= 2

    return (state[7] - state[13]) % MODULUS


def runTests():
    assert polygonSubsetCountModerate(5) == 7
    assert polygonSubsetCount(5) == 7
    assert polygonSubsetCount(10) == 501
    assert polygonSubsetCount(25) == 18635853


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = polygonSubsetCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
