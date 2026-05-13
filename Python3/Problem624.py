import time


MODULUS = 1_000_000_009


def matrixMultiply(left, right, modulus):
    return [
        [
            (left[0][0] * right[0][0] + left[0][1] * right[1][0]) % modulus,
            (left[0][0] * right[0][1] + left[0][1] * right[1][1]) % modulus,
        ],
        [
            (left[1][0] * right[0][0] + left[1][1] * right[1][0]) % modulus,
            (left[1][0] * right[0][1] + left[1][1] * right[1][1]) % modulus,
        ],
    ]


def matrixPower(matrix, exponent, modulus):
    result = [[1, 0], [0, 1]]
    while exponent:
        if exponent % 2:
            result = matrixMultiply(result, matrix, modulus)
        matrix = matrixMultiply(matrix, matrix, modulus)
        exponent //= 2
    return result


def inverse2By2(matrix, modulus):
    determinant = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % modulus
    inverse_determinant = pow(determinant, modulus - 2, modulus)
    return [
        [matrix[1][1] * inverse_determinant % modulus, -matrix[0][1] * inverse_determinant % modulus],
        [-matrix[1][0] * inverse_determinant % modulus, matrix[0][0] * inverse_determinant % modulus],
    ]


def probabilityResidue(n, prime):
    fibonacci_matrix = [[1, 1], [1, 0]]
    scaled = matrixPower(fibonacci_matrix, n, prime)
    scale = pow(pow(2, n, prime), prime - 2, prime)
    scaled = [[value * scale % prime for value in row] for row in scaled]
    complement = [[(1 - scaled[0][0]) % prime, -scaled[0][1] % prime], [-scaled[1][0] % prime, (1 - scaled[1][1]) % prime]]
    total = matrixMultiply(scaled, inverse2By2(complement, prime), prime)
    return total[1][1]


def runTests():
    assert probabilityResidue(2, 109) == 66
    assert probabilityResidue(3, 109) == 46


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = probabilityResidue(10 ** 18, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
