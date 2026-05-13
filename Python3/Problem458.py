import time


LIMIT = 10**12
MODULUS = 10**9


def matrixMultiply(first, second):
    size = len(first)

    return [
        [
            sum(first[row][index] * second[index][column] for index in range(size))
            % MODULUS
            for column in range(size)
        ]
        for row in range(size)
    ]


def vectorMultiply(vector, matrix):
    return [
        sum(vector[index] * matrix[index][column] for index in range(len(vector))) % MODULUS
        for column in range(len(vector))
    ]


def projectFreeStringCount(length=LIMIT):
    transition = [[0] * 7 for _ in range(7)]

    for suffixLength in range(7):
        if suffixLength == 0:
            transition[0][1] = 7
        else:
            for nextLength in range(1, suffixLength + 1):
                transition[suffixLength][nextLength] += 1

            if suffixLength < 6:
                transition[suffixLength][suffixLength + 1] += 7 - suffixLength

    vector = [1, 0, 0, 0, 0, 0, 0]
    exponent = length

    while exponent:
        if exponent & 1:
            vector = vectorMultiply(vector, transition)

        exponent //= 2

        if exponent:
            transition = matrixMultiply(transition, transition)

    return sum(vector) % MODULUS


def runTests():
    assert projectFreeStringCount(7) == 7**7 - 5040


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = projectFreeStringCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
