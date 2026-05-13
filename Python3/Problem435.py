import time


LIMIT = 10**15
MODULUS = 1_307_674_368_000


def matrixMultiply(first, second, modulus):
    size = len(first)

    return [
        [
            sum(first[row][index] * second[index][column] for index in range(size))
            % modulus
            for column in range(size)
        ]
        for row in range(size)
    ]


def matrixVectorMultiply(matrix, vector, modulus):
    return [
        sum(matrix[row][index] * vector[index] for index in range(len(vector))) % modulus
        for row in range(len(vector))
    ]


def fibonacciPolynomial(n, x, modulus=MODULUS):
    if n == 0 or x == 0:
        return 0

    x %= modulus
    xSquared = x * x % modulus
    transition = (
        [1, x, xSquared],
        [0, x, xSquared],
        [0, 1, 0],
    )
    vector = [x, x, 0]
    exponent = n - 1

    while exponent:
        if exponent & 1:
            vector = matrixVectorMultiply(transition, vector, modulus)

        exponent //= 2

        if exponent:
            transition = matrixMultiply(transition, transition, modulus)

    return vector[0]


def polynomialSum(limit=LIMIT):
    return sum(fibonacciPolynomial(limit, x) for x in range(101)) % MODULUS


def runTests():
    assert fibonacciPolynomial(7, 11) == 268357683


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = polynomialSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
