from math import cos, pi, sqrt
import time


QUADRATURE_ORDER = 48


def gaussLegendre(order):
    nodes = [0.0] * order
    weights = [0.0] * order
    tolerance = 1e-15

    for index in range((order + 1) // 2):
        root = cos(pi * (index + 0.75) / (order + 0.5))

        while True:
            p1 = 1.0
            p2 = 0.0
            for degree in range(1, order + 1):
                p3 = p2
                p2 = p1
                p1 = ((2 * degree - 1) * root * p2 - (degree - 1) * p3) / degree

            derivative = order * (root * p1 - p2) / (root * root - 1)
            nextRoot = root - p1 / derivative
            if abs(nextRoot - root) < tolerance:
                root = nextRoot
                break
            root = nextRoot

        nodes[index] = -root
        nodes[order - 1 - index] = root
        weight = 2 / ((1 - root * root) * derivative * derivative)
        weights[index] = weight
        weights[order - 1 - index] = weight

    return nodes, weights


def unitCellDistanceIntegrals(size, order=QUADRATURE_ORDER):
    nodes, weights = gaussLegendre(order)
    positiveNodes = [(node + 1) / 2 for node in nodes]
    positiveWeights = [
        weights[index] * (1 - positiveNodes[index]) / 2
        for index in range(order)
    ]
    pairs = list(zip(positiveNodes, positiveWeights))
    integrals = [[0.0] * size for _ in range(size)]

    for dx in range(size):
        for dy in range(size):
            total = 0.0
            for u, uWeight in pairs:
                xPlus = dx + u
                xMinus = dx - u
                for v, vWeight in pairs:
                    yPlus = dy + v
                    yMinus = dy - v
                    weight = uWeight * vWeight
                    total += weight * (
                        sqrt(xPlus * xPlus + yPlus * yPlus)
                        + sqrt(xPlus * xPlus + yMinus * yMinus)
                        + sqrt(xMinus * xMinus + yPlus * yPlus)
                        + sqrt(xMinus * xMinus + yMinus * yMinus)
                    )
            integrals[dx][dy] = total

    return integrals


def rectangleIntegral(width, height, integrals):
    total = 0.0

    for dx in range(width):
        xMultiplicity = 1 if dx == 0 else 2
        xCount = width - dx
        for dy in range(height):
            yMultiplicity = 1 if dy == 0 else 2
            total += (
                xMultiplicity
                * yMultiplicity
                * xCount
                * (height - dy)
                * integrals[dx][dy]
            )

    return total


def squareToCellIntegrals(size, integrals):
    totals = [[0.0] * size for _ in range(size)]

    for cellX in range(size):
        for cellY in range(size):
            total = 0.0
            for squareX in range(size):
                for squareY in range(size):
                    total += integrals[abs(squareX - cellX)][abs(squareY - cellY)]
            totals[cellX][cellY] = total

    return totals


def buildPrefixSums(grid):
    size = len(grid)
    prefix = [[0.0] * (size + 1) for _ in range(size + 1)]

    for row in range(size):
        rowTotal = 0.0
        for column in range(size):
            rowTotal += grid[row][column]
            prefix[row + 1][column + 1] = prefix[row][column + 1] + rowTotal

    return prefix


def rectangleSum(prefix, left, bottom, width, height):
    right = left + width
    top = bottom + height
    return (
        prefix[right][top]
        - prefix[left][top]
        - prefix[right][bottom]
        + prefix[left][bottom]
    )


def hollowSquareDistanceSum(size):
    integrals = unitCellDistanceIntegrals(size)
    outerIntegral = rectangleIntegral(size, size, integrals)
    crossPrefix = buildPrefixSums(squareToCellIntegrals(size, integrals))
    holeIntegrals = {
        (width, height): rectangleIntegral(width, height, integrals)
        for width in range(1, size - 1)
        for height in range(1, size - 1)
    }

    total = 0.0
    for width in range(1, size - 1):
        for height in range(1, size - 1):
            holeIntegral = holeIntegrals[(width, height)]
            area = size * size - width * height
            inverseAreaSquared = 1 / (area * area)

            for left in range(1, size - width):
                for bottom in range(1, size - height):
                    crossIntegral = rectangleSum(
                        crossPrefix, left, bottom, width, height
                    )
                    total += (
                        outerIntegral - 2 * crossIntegral + holeIntegral
                    ) * inverseAreaSquared

    return total


def runTests():
    assert format(hollowSquareDistanceSum(3), ".4f") == "1.6514"
    assert format(hollowSquareDistanceSum(4), ".4f") == "19.6564"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(hollowSquareDistanceSum(40), ".4f")
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
