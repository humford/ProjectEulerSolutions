import math
import time
from fractions import Fraction


def solveLinearFractions(matrix):
    n = len(matrix)

    for column in range(n):
        pivot = column
        while matrix[pivot][column] == 0:
            pivot += 1
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]

        pivotValue = matrix[column][column]
        for j in range(column, n + 1):
            matrix[column][j] /= pivotValue

        for row in range(n):
            if row == column:
                continue
            factor = matrix[row][column]
            if factor == 0:
                continue
            for j in range(column, n + 1):
                matrix[row][j] -= factor * matrix[column][j]

    return [matrix[i][-1] for i in range(n)]


def SFraction(n):
    length = 2 * n
    stateCount = length - 1
    matrix = [[Fraction(0) for _ in range(stateCount + 1)] for __ in range(stateCount)]

    def index(distance):
        return distance - 1

    for distance in range(1, stateCount + 1):
        row = matrix[index(distance)]
        row[index(distance)] = Fraction(1)

        if distance == 1:
            row[-1] = Fraction(1)
        elif distance == 2:
            row[index(length - 1)] += Fraction(1, 3)
            row[-1] = Fraction(1)
        elif distance == 3:
            row[index(length - 2)] += Fraction(1, 3)
            row[index(length - 1)] += Fraction(1, 3)
            row[-1] = Fraction(1)
        else:
            for roll in (1, 2, 3):
                row[index(length - distance + roll)] += Fraction(1, 3)
            row[-1] = Fraction(1)

    solution = solveLinearFractions(matrix)
    return 2 * solution[index(n)] - 1


def solveLinear4(matrix, rhs):
    augmented = [matrix[i][:] + [rhs[i]] for i in range(4)]

    for column in range(4):
        pivot = max(range(column, 4), key=lambda row: abs(augmented[row][column]))
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]

        pivotValue = augmented[column][column]
        for j in range(column, 5):
            augmented[column][j] /= pivotValue

        for row in range(4):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0.0:
                continue
            for j in range(column, 5):
                augmented[row][j] -= factor * augmented[column][j]

    return [augmented[i][-1] for i in range(4)]


def SFast(n):
    if n == 2:
        return float(SFraction(2))

    length = 2 * n
    q = -2.0 + math.sqrt(3.0)

    def row(distance):
        return [1.0, float(distance), q ** distance, q ** (length - distance)]

    def addScaled(dst, scale, src):
        for i in range(4):
            dst[i] += scale * src[i]

    matrix = []
    rhs = []

    equation = [0.0] * 4
    addScaled(equation, 1.0, row(2))
    addScaled(equation, 1.0 / 3.0, row(length - 1))
    matrix.append(equation)
    rhs.append(1.0)

    equation = [0.0] * 4
    addScaled(equation, 1.0, row(3))
    addScaled(equation, 1.0 / 3.0, row(length - 2))
    addScaled(equation, 1.0 / 3.0, row(length - 1))
    matrix.append(equation)
    rhs.append(1.0)

    equation = [0.0] * 4
    addScaled(equation, 1.0, row(length - 1))
    addScaled(equation, 1.0 / 3.0, row(2))
    addScaled(equation, 1.0 / 3.0, row(3))
    addScaled(equation, 1.0 / 3.0, row(4))
    matrix.append(equation)
    rhs.append(1.0)

    equation = [0.0] * 4
    addScaled(equation, 1.0, row(length - 2))
    addScaled(equation, 1.0 / 3.0, row(3))
    addScaled(equation, 1.0 / 3.0, row(4))
    addScaled(equation, 1.0 / 3.0, row(5))
    matrix.append(equation)
    rhs.append(1.0)

    A, B, C, E = solveLinear4(matrix, rhs)
    winProbability = A + B * n + C * (q ** n) + E * (q ** n)
    return 2.0 * winProbability - 1.0


def digamma(x):
    result = 0.0
    while x < 8.0:
        result -= 1.0 / x
        x += 1.0

    inverse = 1.0 / x
    inverseSquared = inverse * inverse

    result += math.log(x) - 0.5 * inverse
    term = inverseSquared
    result -= term / 12.0
    term *= inverseSquared
    result += term / 120.0
    term *= inverseSquared
    result -= term / 252.0
    term *= inverseSquared
    result += term / 240.0
    term *= inverseSquared
    result -= term / 132.0
    term *= inverseSquared
    result += term * (691.0 / 32760.0)

    return result


def shiftedHarmonicSum(n, shift):
    return digamma(float(n) + shift) - digamma(1.0 + shift)


def correctionConstant(limit=60):
    shift = (3.0 - math.sqrt(3.0)) / 6.0
    total = 0.0
    for n in range(2, limit + 1):
        total += SFast(n) - 1.0 / (n - 1 + shift)
    return total


def T(n):
    shift = (3.0 - math.sqrt(3.0)) / 6.0
    return shiftedHarmonicSum(n, shift) + correctionConstant()


def formattedT(n):
    return f"{T(n):.8f}"


def runTests():
    assert SFraction(2) == Fraction(7, 11)
    exactT10 = sum(SFraction(n) for n in range(2, 11))
    assert Fraction(2_382_352_815, 10 ** 9) <= exactT10 < Fraction(2_382_352_825, 10 ** 9)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedT(10 ** 14)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
