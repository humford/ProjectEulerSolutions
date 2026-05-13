import time
from fractions import Fraction


MODULUS = 1_000_000_007
TOTIENT = MODULUS - 1
X_POINT = (Fraction(7), Fraction(1))


def hyperbolaValue(point):
    x, y = point
    return 12 * x * x + 7 * x * y - 12 * y * y - 625


def nextPoint(previous2, previous1):
    vx = previous2[0] - X_POINT[0]
    vy = previous2[1] - X_POINT[1]
    x, y = previous1
    quadratic = 12 * vx * vx + 7 * vx * vy - 12 * vy * vy
    linear = 24 * x * vx + 7 * (x * vy + y * vx) - 24 * y * vy
    parameter = -linear / quadratic

    return x + parameter * vx, y + parameter * vy


def sequencePoint(index):
    points = [
        None,
        (Fraction(13), Fraction(61, 4)),
        (Fraction(-43, 6), Fraction(-4)),
    ]

    for pointIndex in range(3, index + 1):
        points.append(nextPoint(points[pointIndex - 2], points[pointIndex - 1]))

    return points[index]


def hyperbolaParameter(point):
    x, y = point

    return (3 * x + 4 * y) / 25


def answerForPoint(point):
    x, y = point
    return (x.numerator + x.denominator + y.numerator + y.denominator) % MODULUS


def multiplyMatrices(left, right, modulus):
    return (
        (
            (left[0][0] * right[0][0] + left[0][1] * right[1][0]) % modulus,
            (left[0][0] * right[0][1] + left[0][1] * right[1][1]) % modulus,
        ),
        (
            (left[1][0] * right[0][0] + left[1][1] * right[1][0]) % modulus,
            (left[1][0] * right[0][1] + left[1][1] * right[1][1]) % modulus,
        ),
    )


def matrixPower(matrix, exponent, modulus):
    result = ((1, 0), (0, 1))

    while exponent:
        if exponent % 2:
            result = multiplyMatrices(result, matrix, modulus)

        exponent //= 2

        if exponent:
            matrix = multiplyMatrices(matrix, matrix, modulus)

    return result


def sequenceExponent(index, first, second, modulus):
    if index == 1:
        return first % modulus
    if index == 2:
        return second % modulus

    recurrence = ((-1 % modulus, 1), (1, 0))
    power = matrixPower(recurrence, index - 2, modulus)

    return (
        power[0][0] * (second % modulus) + power[0][1] * (first % modulus)
    ) % modulus


def fastAnswerForIndex(index):
    if index % 6 != 1:
        raise ValueError("this reduced formula is for indices congruent to 1 mod 6")

    twoExponent = sequenceExponent(index, 2, -1, TOTIENT)
    threeExponent = -sequenceExponent(index, 0, 1, TOTIENT) % TOTIENT
    xNumerator = (
        pow(2, (2 * twoExponent - 2) % TOTIENT, MODULUS)
        + pow(3, (2 * threeExponent - 1) % TOTIENT, MODULUS)
    ) % MODULUS
    xDenominator = (
        pow(2, (twoExponent - 2) % TOTIENT, MODULUS)
        * pow(3, (threeExponent - 1) % TOTIENT, MODULUS)
    ) % MODULUS
    yNumerator = (
        pow(2, (2 * twoExponent + 2) % TOTIENT, MODULUS)
        - pow(3, (2 * threeExponent + 1) % TOTIENT, MODULUS)
    ) % MODULUS
    yDenominator = (
        pow(2, twoExponent, MODULUS) * pow(3, threeExponent, MODULUS)
    ) % MODULUS

    return (xNumerator + xDenominator + yNumerator + yDenominator) % MODULUS


def runTests():
    assert sequencePoint(3) == (Fraction(-19, 2), Fraction(-229, 24))
    assert sequencePoint(4) == (Fraction(1267, 144), Fraction(-37, 12))
    assert sequencePoint(7) == (
        Fraction(17194218091, 143327232),
        Fraction(274748766781, 1719926784),
    )
    assert hyperbolaParameter(sequencePoint(1)) == 4
    assert hyperbolaParameter(sequencePoint(2)) == Fraction(-3, 2)
    assert hyperbolaParameter(sequencePoint(7)) == Fraction(2**18, 3**8)
    assert answerForPoint(sequencePoint(7)) == 806236837
    assert fastAnswerForIndex(7) == 806236837
    assert hyperbolaValue(sequencePoint(7)) == 0


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fastAnswerForIndex(11**14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
