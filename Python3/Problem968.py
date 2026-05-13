from itertools import combinations, product
import time


MODULUS = 1_000_000_007
BASES = (2, 3, 5, 7, 11)
TARGET = 100

CONSTRAINTS = (
    (1, 1, 0, 0, 0),
    (1, 0, 1, 0, 0),
    (1, 0, 0, 1, 0),
    (1, 0, 0, 0, 1),
    (0, 1, 1, 0, 0),
    (0, 1, 0, 1, 0),
    (0, 1, 0, 0, 1),
    (0, 0, 1, 1, 0),
    (0, 0, 1, 0, 1),
    (0, 0, 0, 1, 1),
    (-1, 0, 0, 0, 0),
    (0, -1, 0, 0, 0),
    (0, 0, -1, 0, 0),
    (0, 0, 0, -1, 0),
    (0, 0, 0, 0, -1),
)


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]

    total = 0
    firstRow = matrix[0]
    for column, value in enumerate(firstRow):
        if value:
            minor = [row[:column] + row[column + 1 :] for row in matrix[1:]]
            total += (-1) ** column * value * determinant(minor)
    return total


def adjugate(matrix):
    size = len(matrix)
    result = [[0] * size for _ in range(size)]

    for rowIndex in range(size):
        for columnIndex in range(size):
            minor = [
                row[:rowIndex] + row[rowIndex + 1 :]
                for index, row in enumerate(matrix)
                if index != columnIndex
            ]
            result[rowIndex][columnIndex] = (
                (-1) ** (rowIndex + columnIndex) * determinant(minor)
            )

    return result


def monomialWeight(exponents):
    result = 1
    for base, exponent in zip(BASES, exponents):
        if exponent >= 0:
            result = result * pow(base, exponent, MODULUS) % MODULUS
        else:
            result = result * pow(pow(base, -exponent, MODULUS), MODULUS - 2, MODULUS)
            result %= MODULUS
    return result


def pointWeight(exponents):
    result = 1
    for base, exponent in zip(BASES, exponents):
        if exponent < 0:
            return 0
        result = result * pow(base, exponent, MODULUS) % MODULUS
    return result


def vertexCones():
    cones = []

    for activeSet in combinations(range(len(CONSTRAINTS)), 5):
        basis = [CONSTRAINTS[index] for index in activeSet]
        det = determinant(basis)
        if det not in (1, -1, 2, -2):
            continue

        adj = adjugate(basis)
        rays = []
        for column in range(5):
            ray = [adj[row][column] for row in range(5)]
            if sum(basis[column][coordinate] * ray[coordinate] for coordinate in range(5)) > 0:
                ray = [-value for value in ray]
            rays.append(ray)

        denominator = 1
        for ray in rays:
            denominator *= pow((1 - monomialWeight(ray)) % MODULUS, MODULUS - 2, MODULUS)
            denominator %= MODULUS

        cones.append((activeSet, det, adj, rays, denominator))

    return cones


VERTEX_CONES = vertexCones()


def coneP(bounds, simpleVerticesOnly=True):
    bounds = list(bounds) + [0] * 5
    total = 0

    for activeSet, det, adj, rays, denominator in VERTEX_CONES:
        activeBounds = [bounds[index] for index in activeSet]
        numeratorPoint = [
            sum(adj[row][column] * activeBounds[column] for column in range(5))
            for row in range(5)
        ]

        isFeasible = True
        equalities = 0
        if det > 0:
            for index, row in enumerate(CONSTRAINTS):
                value = sum(row[coordinate] * numeratorPoint[coordinate] for coordinate in range(5))
                bound = bounds[index] * det
                if value > bound:
                    isFeasible = False
                    break
                equalities += value == bound
        else:
            for index, row in enumerate(CONSTRAINTS):
                value = sum(row[coordinate] * numeratorPoint[coordinate] for coordinate in range(5))
                bound = bounds[index] * det
                if value < bound:
                    isFeasible = False
                    break
                equalities += value == bound

        if not isFeasible or (simpleVerticesOnly and equalities != 5):
            continue

        absDet = abs(det)
        if absDet == 1:
            exponents = [value // det for value in numeratorPoint]
            total = (total + pointWeight(exponents) * denominator) % MODULUS
        else:
            denominatorScaledRays = [[det * value for value in ray] for ray in rays]
            latticeModulus = 2 * absDet
            numerator = 0

            for mask in range(1 << 5):
                trialPoint = [2 * value for value in numeratorPoint]
                for bit in range(5):
                    if mask & (1 << bit):
                        ray = denominatorScaledRays[bit]
                        for coordinate in range(5):
                            trialPoint[coordinate] += ray[coordinate]

                if any(value % latticeModulus for value in trialPoint):
                    continue

                exponents = [value // (2 * det) for value in trialPoint]
                if all(
                    sum(CONSTRAINTS[row][coordinate] * exponents[coordinate] for coordinate in range(5))
                    <= bounds[row]
                    for row in range(len(CONSTRAINTS))
                ):
                    numerator = (numerator + pointWeight(exponents)) % MODULUS

            total = (total + numerator * denominator) % MODULUS

    return total


def bruteP(bounds):
    caps = (
        min(bounds[0], bounds[1], bounds[2], bounds[3]),
        min(bounds[0], bounds[4], bounds[5], bounds[6]),
        min(bounds[1], bounds[4], bounds[7], bounds[8]),
        min(bounds[2], bounds[5], bounds[7], bounds[9]),
        min(bounds[3], bounds[6], bounds[8], bounds[9]),
    )
    total = 0

    for exponents in product(*(range(cap + 1) for cap in caps)):
        if all(
            exponents[left] + exponents[right] <= bound
            for (left, right), bound in zip(
                (
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 4),
                    (1, 2),
                    (1, 3),
                    (1, 4),
                    (2, 3),
                    (2, 4),
                    (3, 4),
                ),
                bounds,
            )
        ):
            total = (total + pointWeight(exponents)) % MODULUS

    return total


def P(bounds):
    caps = (
        min(bounds[0], bounds[1], bounds[2], bounds[3]),
        min(bounds[0], bounds[4], bounds[5], bounds[6]),
        min(bounds[1], bounds[4], bounds[7], bounds[8]),
        min(bounds[2], bounds[5], bounds[7], bounds[9]),
        min(bounds[3], bounds[6], bounds[8], bounds[9]),
    )
    if max(caps) <= 12:
        return bruteP(bounds)
    return coneP(bounds)


def sequenceA(length):
    values = [0] * length
    values[0] = 1
    values[1] = 7
    for index in range(2, length):
        values[index] = (7 * values[index - 1] + values[index - 2] ** 2) % MODULUS
    return values


def Q(values, index):
    return P(values[10 * index : 10 * index + 10])


def S(count):
    values = sequenceA(10 * count + 10)
    return sum(Q(values, index) for index in range(count)) % MODULUS


def solve():
    return S(TARGET)


def runTests():
    assert P([2] * 10) == 7120
    assert P(list(range(1, 11))) == 799_809_376
    assert coneP(list(range(1, 11))) == 799_809_376
    assert sequenceA(3) == [1, 7, 50]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
