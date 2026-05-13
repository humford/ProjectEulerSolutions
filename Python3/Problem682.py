import time


MODULUS = 1_000_000_007
TARGET = 10 ** 7


def trimPolynomial(polynomial):
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def multiplyPolynomials(first, second):
    result = [0] * (len(first) + len(second) - 1)
    for i, firstCoefficient in enumerate(first):
        if firstCoefficient == 0:
            continue
        for j, secondCoefficient in enumerate(second):
            if secondCoefficient:
                result[i + j] = (
                    result[i + j]
                    + firstCoefficient * secondCoefficient
                ) % MODULUS
    return result


def oneMinusPower(power):
    polynomial = [0] * (power + 1)
    polynomial[0] = 1
    polynomial[power] = MODULUS - 1
    return polynomial


def multiplyFactors(factors):
    result = [1]
    for factor in factors:
        result = multiplyPolynomials(result, factor)
    return result


def negateOddCoefficients(polynomial):
    result = polynomial[:]
    for index in range(1, len(result), 2):
        result[index] = (-result[index]) % MODULUS
    return result


def evenPart(polynomial):
    return polynomial[::2]


def oddPart(polynomial):
    result = polynomial[1::2]
    return result if result else [0]


def coefficientOfRationalFunction(numerator, denominator, index):
    numerator = numerator[:]
    denominator = denominator[:]

    while index:
        negativeDenominator = negateOddCoefficients(denominator)
        numerator = multiplyPolynomials(numerator, negativeDenominator)
        denominator = multiplyPolynomials(denominator, negativeDenominator)

        numerator = oddPart(numerator) if index & 1 else evenPart(numerator)
        denominator = evenPart(denominator)
        trimPolynomial(numerator)
        trimPolynomial(denominator)
        index //= 2

    return numerator[0] * pow(denominator[0], MODULUS - 2, MODULUS) % MODULUS


def hammingPairGeneratingFunction():
    firstDenominator = multiplyFactors(
        [oneMinusPower(power) for power in (1, 3, 4, 5, 7)]
    )
    secondDenominator = multiplyFactors(
        [[1, MODULUS - 1], [1, MODULUS - 1], [1, 1]]
        + [oneMinusPower(power) for power in (5, 6, 8)]
    )
    thirdDenominator = multiplyFactors(
        [[1, MODULUS - 1], [1, MODULUS - 1], [1, 1], [1, 1, 1]]
        + [oneMinusPower(power) for power in (7, 8, 10)]
    )

    denominator = multiplyPolynomials(
        multiplyPolynomials(firstDenominator, secondDenominator),
        thirdDenominator,
    )

    firstPart = multiplyPolynomials(secondDenominator, thirdDenominator)

    secondPart = [0] + multiplyPolynomials(firstDenominator, thirdDenominator)
    secondPart = [(-coefficient) % MODULUS for coefficient in secondPart]

    thirdPart = [0] * 5 + multiplyPolynomials(firstDenominator, secondDenominator)

    length = max(len(firstPart), len(secondPart), len(thirdPart))
    numerator = [0] * length
    for index in range(length):
        numerator[index] = (
            (firstPart[index] if index < len(firstPart) else 0)
            + (secondPart[index] if index < len(secondPart) else 0)
            + (thirdPart[index] if index < len(thirdPart) else 0)
        ) % MODULUS

    trimPolynomial(numerator)
    trimPolynomial(denominator)
    return numerator, denominator


def hammingPairCount(totalPrimeSum):
    numerator, denominator = hammingPairGeneratingFunction()
    return coefficientOfRationalFunction(numerator, denominator, totalPrimeSum)


def runTests():
    assert hammingPairCount(10) == 4
    assert hammingPairCount(10 ** 2) == 3_629


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hammingPairCount(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
