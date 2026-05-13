import time


MODULUS = 1_117_117_717
TARGET_EXPONENT = 10 ** 9


def addedOnes(number):
    total = 0
    while number > 1:
        if number % 7 == 0:
            number //= 7
        else:
            number += 1
            total += 1
    return total


def oneOverElevenBaseSevenPeriod():
    remainder = 1
    digits = []
    for _ in range(10):
        remainder *= 7
        digits.append(remainder // 11)
        remainder %= 11

    assert remainder == 1
    return digits


def digitMatrix(digit, modulus):
    # State: [S(m), g(m + 1), m, 1], updated after appending base-7 digit.
    partialBlockOffset = -6 + 7 * digit - digit * (digit + 1) // 2
    nextGap = 0 if digit == 6 else 6 - digit

    return [
        [7 % modulus, digit % modulus, 21 % modulus, partialBlockOffset % modulus],
        [0, 1, 0, nextGap % modulus],
        [0, 0, 7 % modulus, digit % modulus],
        [0, 0, 0, 1],
    ]


def multiplyMatrices(left, right, modulus):
    size = len(left)
    result = [[0] * size for _ in range(size)]
    for row in range(size):
        for middle in range(size):
            value = left[row][middle]
            if value == 0:
                continue
            for column in range(size):
                result[row][column] += value * right[middle][column]
        for column in range(size):
            result[row][column] %= modulus
    return result


def matrixPower(matrix, exponent, modulus):
    size = len(matrix)
    result = [
        [1 if row == column else 0 for column in range(size)]
        for row in range(size)
    ]
    power = matrix
    while exponent:
        if exponent & 1:
            result = multiplyMatrices(result, power, modulus)
        exponent //= 2
        if exponent:
            power = multiplyMatrices(power, power, modulus)
    return result


def multiplyMatrixVector(matrix, vector, modulus):
    return [
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        % modulus
        for row in range(len(matrix))
    ]


def oneMoreOneSum(exponent, modulus=MODULUS):
    if exponent % 10 != 0:
        raise ValueError("exponent must be divisible by the base-7 period length")

    period = oneOverElevenBaseSevenPeriod()
    assert period == [0, 4, 3, 1, 1, 6, 2, 3, 5, 5]

    # Dropping the leading zero leaves the base-7 digits of (7^K - 1) / 11.
    digitBlock = period[1:] + period[:1]
    fullBlocks, remainingDigits = divmod(exponent - 1, len(digitBlock))

    blockMatrix = [
        [1 if row == column else 0 for column in range(4)]
        for row in range(4)
    ]
    for digit in digitBlock:
        blockMatrix = multiplyMatrices(
            digitMatrix(digit, modulus),
            blockMatrix,
            modulus,
        )

    state = [0, 0, 0, 1]
    state = multiplyMatrixVector(
        matrixPower(blockMatrix, fullBlocks, modulus),
        state,
        modulus,
    )

    for digit in digitBlock[:remainingDigits]:
        state = multiplyMatrixVector(digitMatrix(digit, modulus), state, modulus)

    return state[0]


def runTests():
    assert addedOnes(125) == 8
    assert addedOnes(1_000) == 9
    assert addedOnes(10_000) == 21
    assert oneMoreOneSum(10, 10 ** 18) == 690_409_338


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = oneMoreOneSum(TARGET_EXPONENT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
