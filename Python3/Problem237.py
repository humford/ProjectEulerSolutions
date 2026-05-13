import time


MODULUS = 100000000


def multiply(first, second, modulus):
    size = len(first)
    result = [[0] * size for _ in range(size)]

    for i in range(size):
        for k in range(size):
            if first[i][k] == 0:
                continue
            for j in range(size):
                result[i][j] = (
                    result[i][j] + first[i][k] * second[k][j]
                ) % modulus

    return result


def power(matrix, exponent, modulus):
    size = len(matrix)
    result = [[int(i == j) for j in range(size)] for i in range(size)]

    while exponent:
        if exponent % 2:
            result = multiply(result, matrix, modulus)
        matrix = multiply(matrix, matrix, modulus)
        exponent //= 2

    return result


def tourCount(n, modulus=MODULUS):
    initial = [8, 4, 1, 1]
    if n <= 4:
        return [0, 1, 1, 4, 8][n] % modulus

    transition = [
        [2, 2, -2, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
    matrix = power(transition, n - 4, modulus)
    return sum(matrix[0][index] * initial[index] for index in range(4)) % modulus


def runTests():
    assert tourCount(10) == 2329


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = tourCount(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
