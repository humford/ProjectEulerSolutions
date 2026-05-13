import time


BINOMIAL_CACHE = {}


def monotoneMatrices(rows, columns, maxValue):
    matrix = [[0] * columns for _ in range(rows)]

    def recurse(position):
        if position == rows * columns:
            yield tuple(tuple(row) for row in matrix)
            return

        row, column = divmod(position, columns)
        minimum = 0
        if row > 0:
            minimum = max(minimum, matrix[row - 1][column])
        if column > 0:
            minimum = max(minimum, matrix[row][column - 1])

        for value in range(minimum, maxValue + 1):
            matrix[row][column] = value
            yield from recurse(position + 1)

    yield from recurse(0)


def binomial(n, k):
    if n < 0 or k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1

    k = min(k, n - k)
    key = (n, k)
    cached = BINOMIAL_CACHE.get(key)
    if cached is not None:
        return cached

    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i

    BINOMIAL_CACHE[key] = result
    return result


def bareissDeterminant(matrix):
    size = len(matrix)
    if size == 0:
        return 1
    if size == 1:
        return matrix[0][0]

    values = [row[:] for row in matrix]
    sign = 1
    previousPivot = 1

    for pivotIndex in range(size - 1):
        if values[pivotIndex][pivotIndex] == 0:
            swapIndex = None
            for row in range(pivotIndex + 1, size):
                if values[row][pivotIndex] != 0:
                    swapIndex = row
                    break
            if swapIndex is None:
                return 0
            values[pivotIndex], values[swapIndex] = values[swapIndex], values[pivotIndex]
            sign = -sign

        pivot = values[pivotIndex][pivotIndex]
        for row in range(pivotIndex + 1, size):
            for column in range(pivotIndex + 1, size):
                values[row][column] = (
                    values[row][column] * pivot - values[row][pivotIndex] * values[pivotIndex][column]
                ) // previousPivot
        previousPivot = pivot
        for row in range(pivotIndex + 1, size):
            values[row][pivotIndex] = 0

    return sign * values[size - 1][size - 1]


def countOctagonTilings(a, b, c, d):
    xMatrices = list(monotoneMatrices(b, d, a))
    yMatrices = []
    for reversedY in monotoneMatrices(b, d, c):
        y = tuple(tuple(reversedY[b - 1 - row][column] for column in range(d)) for row in range(b))
        yMatrices.append(y)

    total = 0

    for x in xMatrices:
        xFull = [[0] * (d + 2) for _ in range(b + 2)]
        for row in range(1, b + 1):
            for column in range(1, d + 1):
                xFull[row][column] = x[row - 1][column - 1]
        for row in range(1, b + 1):
            xFull[row][d + 1] = a
        for column in range(d + 2):
            xFull[b + 1][column] = a

        for y in yMatrices:
            yFull = [[0] * (d + 2) for _ in range(b + 2)]
            for row in range(1, b + 1):
                for column in range(1, d + 1):
                    yFull[row][column] = y[row - 1][column - 1]
            for row in range(1, b + 1):
                yFull[row][d + 1] = c
            for column in range(d + 2):
                yFull[0][column] = c

            product = 1

            for u in range(1, d + 2):
                determinantMatrix = []
                for i in range(1, b + 1):
                    determinantRow = []
                    for j in range(1, b + 1):
                        pathLength = (xFull[j][u] - xFull[i][u - 1]) + (yFull[j][u] - yFull[i][u - 1])
                        horizontalSteps = (xFull[j][u] - xFull[i][u - 1]) + (j - i)
                        determinantRow.append(binomial(pathLength, horizontalSteps))
                    determinantMatrix.append(determinantRow)

                product *= bareissDeterminant(determinantMatrix)
                if product == 0:
                    break
            if product == 0:
                continue

            for v in range(1, b + 2):
                determinantMatrix = []
                for i in range(1, d + 1):
                    determinantRow = []
                    for j in range(1, d + 1):
                        pathLength = (xFull[v][j] - xFull[v - 1][i]) + (yFull[v - 1][i] - yFull[v][j])
                        horizontalSteps = (xFull[v][j] - xFull[v - 1][i]) + (j - i)
                        determinantRow.append(binomial(pathLength, horizontalSteps))
                    determinantMatrix.append(determinantRow)

                product *= bareissDeterminant(determinantMatrix)
                if product == 0:
                    break

            total += product

    return total


def rhombusTilings(a, b):
    return countOctagonTilings(a, b, a, b)


def runTests():
    assert rhombusTilings(1, 1) == 8
    assert rhombusTilings(2, 1) == 76
    assert rhombusTilings(3, 2) == 456_572


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rhombusTilings(4, 2)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
