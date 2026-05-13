import time


MODULUS = 1_000_000_007


def divisibleSubstringCount(number):
    counts = [1, 0, 0]
    prefix = 0
    total = 0

    for digit in str(number):
        prefix = (prefix + ord(digit) - ord("0")) % 3
        total += counts[prefix]
        counts[prefix] += 1

    return total


def stateIndex(count0, count1, count2, prefix):
    return ((count0 * 3 + count1) * 3 + count2) * 3 + prefix


def multiplyMatrices(left, right):
    size = len(left)
    result = [[0] * size for _ in range(size)]

    for i in range(size):
        resultRow = result[i]
        leftRow = left[i]
        for k in range(size):
            leftValue = leftRow[k]
            if not leftValue:
                continue

            rightRow = right[k]
            for j in range(size):
                rightValue = rightRow[j]
                if rightValue:
                    resultRow[j] = (resultRow[j] + leftValue * rightValue) % MODULUS

    return result


def powerMatrix(matrix, exponent):
    size = len(matrix)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        result[i][i] = 1

    base = matrix
    while exponent:
        if exponent & 1:
            result = multiplyMatrices(base, result)
        exponent >>= 1
        if exponent:
            base = multiplyMatrices(base, base)

    return result


def multiplyMatrixVector(matrix, vector):
    result = [0] * len(vector)

    for i, row in enumerate(matrix):
        total = 0
        for j, value in enumerate(row):
            if value:
                total = (total + value * vector[j]) % MODULUS
        result[i] = total

    return result


def buildStepMatrix(weights):
    size = 81
    matrix = [[0] * size for _ in range(size)]

    for count0 in range(3):
        for count1 in range(3):
            for count2 in range(3):
                for prefix in range(3):
                    start = stateIndex(count0, count1, count2, prefix)

                    for residue, weight in enumerate(weights):
                        nextPrefix = (prefix + residue) % 3
                        next0, next1, next2 = count0, count1, count2
                        if nextPrefix == 0:
                            next0 = (next0 + 1) % 3
                        elif nextPrefix == 1:
                            next1 = (next1 + 1) % 3
                        else:
                            next2 = (next2 + 1) % 3

                        end = stateIndex(next0, next1, next2, nextPrefix)
                        matrix[end][start] = (matrix[end][start] + weight) % MODULUS

    return matrix


def goodStates():
    good = [False] * 81

    for count0 in range(3):
        for count1 in range(3):
            for count2 in range(3):
                twos = (1 if count0 == 2 else 0) + (1 if count1 == 2 else 0) + (1 if count2 == 2 else 0)
                if twos % 3 == 0:
                    for prefix in range(3):
                        good[stateIndex(count0, count1, count2, prefix)] = True

    return good


def threeLikeCount(digits):
    if digits <= 0:
        return 0

    leadingStep = buildStepMatrix([3, 3, 3])
    ordinaryStep = buildStepMatrix([4, 3, 3])
    vector = [0] * 81
    vector[stateIndex(1, 0, 0, 0)] = 1
    vector = multiplyMatrixVector(leadingStep, vector)

    if digits > 1:
        vector = multiplyMatrixVector(powerMatrix(ordinaryStep, digits - 1), vector)

    good = goodStates()
    return sum(vector[i] for i in range(81) if good[i]) % MODULUS


def runTests():
    assert divisibleSubstringCount(2573) == 3
    assert threeLikeCount(2) == 30
    assert threeLikeCount(6) == 290_898


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = threeLikeCount(10 ** 5)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
