import time


MODULUS = 10**9
STATE_SIZE = 18


def multiplyMatrices(left, right):
    return [
        [
            sum(left[row][index] * right[index][column] for index in range(STATE_SIZE))
            % MODULUS
            for column in range(STATE_SIZE)
        ]
        for row in range(STATE_SIZE)
    ]


def multiplyMatrixVector(matrix, vector):
    return [
        sum(matrix[row][column] * vector[column] for column in range(STATE_SIZE)) % MODULUS
        for row in range(STATE_SIZE)
    ]


def transitionMatrix():
    matrix = [[0] * STATE_SIZE for _ in range(STATE_SIZE)]

    for index in range(9):
        matrix[0][index] = 1
        matrix[9][index] = index + 1
        matrix[9][9 + index] = 10

    for index in range(1, 9):
        matrix[index][index - 1] = 1

    for index in range(10, 18):
        matrix[index][index - 1] = 1

    return matrix


def matrixPower(matrix, exponent):
    result = [[1 if row == column else 0 for column in range(STATE_SIZE)] for row in range(STATE_SIZE)]

    while exponent > 0:
        if exponent & 1:
            result = multiplyMatrices(result, matrix)

        matrix = multiplyMatrices(matrix, matrix)
        exponent //= 2

    return result


TRANSITION = transitionMatrix()


def digitSumNumberSum(digitSum):
    initial = [0] * STATE_SIZE
    initial[0] = 1
    return multiplyMatrixVector(matrixPower(TRANSITION, digitSum), initial)[9]


def experience13Sum():
    return sum(digitSumNumberSum(13**power) for power in range(1, 18)) % MODULUS


def runTests():
    assert digitSumNumberSum(5) == 17891


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = experience13Sum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
