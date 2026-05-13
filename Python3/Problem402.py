import math
import time


LIMIT = 1_234_567_890_123
MODULUS = 10**9
PERIOD = 24
LUCAS_24 = 103682
MONOMIALS = [
    (0, 0),
    (1, 0),
    (0, 1),
    (2, 0),
    (1, 1),
    (0, 2),
    (3, 0),
    (2, 1),
    (1, 2),
    (0, 3),
]
MONOMIAL_INDEX = {monomial: index for index, monomial in enumerate(MONOMIALS)}
MATRIX_SIZE = len(MONOMIALS) + 1


def polynomialValue(n, a, b, c):
    return n**4 + a * n**3 + b * n**2 + c * n


def maximumDivisor(a, b, c):
    return math.gcd(24, 36 + 6 * a, 14 + 6 * a + 2 * b, 1 + a + b + c)


def bruteMaximumDivisor(a, b, c):
    value = 0

    for n in range(1, 6):
        value = math.gcd(value, polynomialValue(n, a, b, c))

    return value


def coefficientsByRemainder(remainder, modulus=None):
    coefficients = [0, 0, 0, 0]

    for a in range(1, PERIOD + 1):
        aExtra = 1 if a <= remainder else 0

        for b in range(1, PERIOD + 1):
            bExtra = 1 if b <= remainder else 0

            for c in range(1, PERIOD + 1):
                cExtra = 1 if c <= remainder else 0
                value = maximumDivisor(a, b, c)
                coefficients[3] += value
                coefficients[2] += value * (aExtra + bExtra + cExtra)
                coefficients[1] += value * (
                    aExtra * bExtra + aExtra * cExtra + bExtra * cExtra
                )
                coefficients[0] += value * aExtra * bExtra * cExtra

    if modulus is not None:
        coefficients = [coefficient % modulus for coefficient in coefficients]

    return coefficients


def polynomialSum(limit):
    quotient, remainder = divmod(limit, PERIOD)
    coefficients = coefficientsByRemainder(remainder)
    return sum(coefficient * quotient**power for power, coefficient in enumerate(coefficients))


def fibonacciNumber(index):
    if index == 0:
        return 0, 1

    previous, current = fibonacciNumber(index // 2)
    doubled = previous * (2 * current - previous)
    squared = previous * previous + current * current

    if index % 2 == 1:
        return squared, doubled + squared

    return doubled, squared


def multiplyPolynomials(left, right):
    product = {}

    for (leftX, leftY), leftValue in left.items():
        for (rightX, rightY), rightValue in right.items():
            key = (leftX + rightX, leftY + rightY)
            product[key] = (product.get(key, 0) + leftValue * rightValue) % MODULUS

    return product


def polynomialPower(base, exponent):
    result = {(0, 0): 1}

    for _ in range(exponent):
        result = multiplyPolynomials(result, base)

    return result


def transitionMatrix(remainder, coefficients):
    matrix = [[0] * MATRIX_SIZE for _ in range(MATRIX_SIZE)]
    constant = ((LUCAS_24 - 2) * remainder // PERIOD) % MODULUS
    nextX = {(0, 1): 1}
    nextY = {(1, 0): -1 % MODULUS, (0, 1): LUCAS_24 % MODULUS, (0, 0): constant}

    for row, (xPower, yPower) in enumerate(MONOMIALS):
        polynomial = multiplyPolynomials(
            polynomialPower(nextX, xPower), polynomialPower(nextY, yPower)
        )

        for monomial, value in polynomial.items():
            matrix[row][MONOMIAL_INDEX[monomial]] = value

    accumulator = MATRIX_SIZE - 1
    matrix[accumulator][accumulator] = 1

    for power, coefficient in enumerate(coefficients):
        matrix[accumulator][MONOMIAL_INDEX[(0, power)]] = (
            matrix[accumulator][MONOMIAL_INDEX[(0, power)]] + coefficient
        ) % MODULUS

    return matrix


def multiplyMatrices(left, right):
    product = [[0] * MATRIX_SIZE for _ in range(MATRIX_SIZE)]

    for row in range(MATRIX_SIZE):
        for middle, leftValue in enumerate(left[row]):
            if leftValue == 0:
                continue

            for column, rightValue in enumerate(right[middle]):
                if rightValue:
                    product[row][column] = (
                        product[row][column] + leftValue * rightValue
                    ) % MODULUS

    return product


def multiplyMatrixVector(matrix, vector):
    return [
        sum(value * entry for value, entry in zip(row, vector)) % MODULUS
        for row in matrix
    ]


def applyMatrixPower(matrix, exponent, vector):
    while exponent > 0:
        if exponent % 2 == 1:
            vector = multiplyMatrixVector(matrix, vector)

        matrix = multiplyMatrices(matrix, matrix)
        exponent //= 2

    return vector


def evaluatePolynomial(coefficients, value):
    return sum(
        coefficient * pow(value, power, MODULUS)
        for power, coefficient in enumerate(coefficients)
    ) % MODULUS


def residueClassSum(residue, limit):
    if residue == 0:
        firstIndex = 1
        lastIndex = limit // PERIOD
    elif residue == 1:
        firstIndex = 1
        lastIndex = (limit - 1) // PERIOD
    else:
        firstIndex = 0
        lastIndex = (limit - residue) // PERIOD

    if lastIndex < firstIndex:
        return 0

    termCount = lastIndex - firstIndex + 1
    fibonacciRemainder = fibonacciNumber(residue)[0] % PERIOD
    coefficients = coefficientsByRemainder(fibonacciRemainder, MODULUS)

    def quotientFor(index):
        return (fibonacciNumber(PERIOD * index + residue)[0] - fibonacciRemainder) // PERIOD

    firstQuotient = quotientFor(firstIndex) % MODULUS
    secondQuotient = quotientFor(firstIndex + 1) % MODULUS
    vector = [
        pow(firstQuotient, xPower, MODULUS)
        * pow(secondQuotient, yPower, MODULUS)
        % MODULUS
        for xPower, yPower in MONOMIALS
    ]
    vector.append(evaluatePolynomial(coefficients, firstQuotient))

    matrix = transitionMatrix(fibonacciRemainder, coefficients)
    vector = applyMatrixPower(matrix, termCount - 1, vector)
    return vector[-1]


def fibonacciPolynomialSumLastDigits(limit=LIMIT):
    return sum(residueClassSum(residue, limit) for residue in range(PERIOD)) % MODULUS


def runTests():
    assert maximumDivisor(4, 2, 5) == 6
    assert maximumDivisor(4, 2, 5) == bruteMaximumDivisor(4, 2, 5)
    assert polynomialSum(10) == 1972
    assert polynomialSum(10000) == 2024258331114


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciPolynomialSumLastDigits()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
