import time


EXPONENT = 987654321
MODULUS = 10**8


def multiplyMatrices(left, right):
    return [
        [
            sum(left[row][index] * right[index][column] for index in range(3))
            % MODULUS
            for column in range(3)
        ]
        for row in range(3)
    ]


def powerMatrix(matrix, exponent):
    result = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    while exponent > 0:
        if exponent & 1:
            result = multiplyMatrices(result, matrix)

        matrix = multiplyMatrices(matrix, matrix)
        exponent //= 2

    return result


def rootPowerSum(index, exponent=EXPONENT):
    coefficient = pow(2, index, MODULUS)

    if exponent == 0:
        return 3

    if exponent == 1:
        return coefficient

    second = coefficient * coefficient % MODULUS

    if exponent == 2:
        return second

    matrix = [
        [coefficient, 0, -index % MODULUS],
        [1, 0, 0],
        [0, 1, 0],
    ]
    powered = powerMatrix(matrix, exponent - 2)

    return (powered[0][0] * second + powered[0][1] * coefficient + powered[0][2] * 3) % MODULUS


def cubicRootPowerFloorSum():
    return sum((rootPowerSum(index) - 1) % MODULUS for index in range(1, 31)) % MODULUS


def runTests():
    assert rootPowerSum(2, 1) - 1 == 3


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cubicRootPowerFloorSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
