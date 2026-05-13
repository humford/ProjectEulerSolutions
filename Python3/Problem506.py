import time


MODULUS = 123_454_321
DIGITS = "123432"
DIGIT_PERIOD = len(DIGITS)
SUM_PERIOD = sum(int(digit) for digit in DIGITS)
POWER_PERIOD = pow(10, DIGIT_PERIOD, MODULUS)


def multiplyMatrices(left, right):
    return [
        [
            sum(left[row][inner] * right[inner][col] for inner in range(3)) % MODULUS
            for col in range(3)
        ]
        for row in range(3)
    ]


def powerMatrix(matrix, exponent):
    result = [[1 if row == col else 0 for col in range(3)] for row in range(3)]

    while exponent:
        if exponent & 1:
            result = multiplyMatrices(matrix, result)

        matrix = multiplyMatrices(matrix, matrix)
        exponent //= 2

    return result


def applyMatrix(matrix, vector):
    return [sum(matrix[row][col] * vector[col] for col in range(3)) % MODULUS for row in range(3)]


def cycleBlock(startIndex):
    return int("".join(DIGITS[(startIndex + offset) % DIGIT_PERIOD] for offset in range(DIGIT_PERIOD)))


def residueClassData():
    data = []
    digitIndex = 0

    for targetSum in range(1, SUM_PERIOD + 1):
        value = 0
        digitSum = 0
        length = 0
        startIndex = digitIndex % DIGIT_PERIOD

        while digitSum < targetSum:
            digit = int(DIGITS[digitIndex % DIGIT_PERIOD])
            digitIndex += 1
            digitSum += digit
            value = value * 10 + digit
            length += 1

        data.append((value % MODULUS, length, cycleBlock(startIndex) % MODULUS))

    return data


def residueClassSum(baseValue, baseLength, blockValue, count):
    blockScale = blockValue * pow(10, baseLength, MODULUS) % MODULUS
    transition = [
        [POWER_PERIOD, 0, 0],
        [blockScale, 1, 0],
        [0, 1, 1],
    ]

    # State is [10^(6q), current_value, cumulative_sum].  Each transition
    # first adds the current value to the sum, then prepends one full cycle.
    finalState = applyMatrix(powerMatrix(transition, count), [1, baseValue, 0])
    return finalState[2]


def clockSequenceSum(limit):
    total = 0

    for residue, (baseValue, baseLength, blockValue) in enumerate(residueClassData(), 1):
        if residue <= limit:
            count = (limit - residue) // SUM_PERIOD + 1
            total += residueClassSum(baseValue, baseLength, blockValue, count)
            total %= MODULUS

    return total


def runTests():
    assert clockSequenceSum(11) == 36_120
    assert clockSequenceSum(1_000) == 18_232_686


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = clockSequenceSum(10**14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
