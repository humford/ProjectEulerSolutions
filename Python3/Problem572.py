import itertools
import math
import time


def ceilDiv(numerator, denominator):
    return -((-numerator) // denominator)


def constrainLinearRange(low, high, coefficient, constant, lowerBound, upperBound):
    if coefficient == 0:
        if lowerBound <= constant <= upperBound:
            return low, high
        return 1, 0

    if coefficient < 0:
        coefficient = -coefficient
        constant = -constant
        lowerBound, upperBound = -upperBound, -lowerBound

    low = max(low, ceilDiv(lowerBound - constant, coefficient))
    high = min(high, (upperBound - constant) // coefficient)
    return low, high


def countTwoVariableSolutions(b, c, total, yRange, zRange):
    yLow, yHigh = yRange
    zLow, zHigh = zRange

    if yLow > yHigh or zLow > zHigh:
        return 0

    if b == 0 and c == 0:
        if total == 0:
            return (yHigh - yLow + 1) * (zHigh - zLow + 1)
        return 0

    if c == 0:
        if total % b:
            return 0
        y = total // b
        return zHigh - zLow + 1 if yLow <= y <= yHigh else 0

    if b == 0:
        if total % c:
            return 0
        z = total // c
        return yHigh - yLow + 1 if zLow <= z <= zHigh else 0

    divisor = math.gcd(abs(b), abs(c))
    if total % divisor:
        return 0

    b //= divisor
    c //= divisor
    total //= divisor
    modulus = abs(c)

    if modulus == 1:
        firstY = 0
    else:
        firstY = (total * pow(b % modulus, -1, modulus)) % modulus

    firstZ = (total - b * firstY) // c
    zStep = -(b * modulus) // c
    low = ceilDiv(yLow - firstY, modulus)
    high = (yHigh - firstY) // modulus
    low, high = constrainLinearRange(low, high, zStep, firstZ, zLow, zHigh)

    return max(0, high - low + 1)


def countDotProductSolutions(vector, ranges):
    widths = [high - low + 1 for low, high in ranges]
    if min(widths) <= 0:
        return 0

    loopIndex = min(range(3), key=lambda index: widths[index])
    otherIndices = [index for index in range(3) if index != loopIndex]
    coefficient = vector[loopIndex]
    low, high = ranges[loopIndex]
    count = 0

    for value in range(low, high + 1):
        count += countTwoVariableSolutions(
            vector[otherIndices[0]],
            vector[otherIndices[1]],
            1 - coefficient * value,
            ranges[otherIndices[0]],
            ranges[otherIndices[1]],
        )

    return count


def productInterval(coefficient, lowerBound, upperBound):
    if coefficient == 0:
        if lowerBound <= 0 <= upperBound:
            return -10 ** 9, 10 ** 9
        return 1, 0

    if coefficient < 0:
        coefficient = -coefficient
        lowerBound, upperBound = -upperBound, -lowerBound

    return ceilDiv(lowerBound, coefficient), upperBound // coefficient


def intersect(first, second):
    return max(first[0], second[0]), min(first[1], second[1])


def rankTwoRanges(vector, limit):
    ranges = []

    for column in range(3):
        valueRange = (-10 ** 9, 10 ** 9)
        for row, coefficient in enumerate(vector):
            if row == column:
                bounds = (1 - limit, limit + 1)
            else:
                bounds = (-limit, limit)
            valueRange = intersect(valueRange, productInterval(coefficient, *bounds))
        ranges.append(valueRange)

    return ranges


def primitiveCanonicalVectors(limit):
    gcd = math.gcd

    for a in range(0, limit + 1):
        bValues = range(-limit, limit + 1) if a else range(0, limit + 1)
        for b in bValues:
            cValues = range(-limit, limit + 1) if (a or b) else range(1, limit + 1)
            for c in cValues:
                if gcd(gcd(abs(a), abs(b)), abs(c)) == 1:
                    yield (a, b, c), max(abs(a), abs(b), abs(c))


def idempotentMatrixCount(limit):
    rankOneCount = 0
    rankTwoCount = 0

    for vector, maximumEntry in primitiveCanonicalVectors(limit + 1):
        if maximumEntry <= limit:
            quotient = limit // maximumEntry
            rankOneCount += countDotProductSolutions(
                vector, [(-quotient, quotient)] * 3
            )

        rankTwoCount += countDotProductSolutions(vector, rankTwoRanges(vector, limit))

    return rankOneCount + rankTwoCount + 2


def isIdempotent(entries):
    matrix = [list(entries[:3]), list(entries[3:6]), list(entries[6:])]
    product = [
        [sum(matrix[row][k] * matrix[k][col] for k in range(3)) for col in range(3)]
        for row in range(3)
    ]
    return product == matrix


def idempotentMatrixCountBrute(limit):
    values = range(-limit, limit + 1)
    return sum(
        1 for entries in itertools.product(values, repeat=9) if isIdempotent(entries)
    )


def runTests():
    assert idempotentMatrixCountBrute(1) == 164
    assert idempotentMatrixCount(1) == 164
    assert idempotentMatrixCount(2) == 848


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = idempotentMatrixCount(200)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
