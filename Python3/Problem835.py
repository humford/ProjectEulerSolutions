from decimal import Decimal, getcontext
import time


MOD = 1_234_567_891
INVERSE_THREE = pow(3, -1, MOD)


def sumLegHypotenuseFamilyForPowerOfTen(exponent):
    if exponent % 2 != 0:
        raise ValueError("expected an even power-of-ten exponent")

    halfExponent = exponent // 2
    count = 5 * pow(10, halfExponent - 1, MOD) % MOD
    count2 = count * count % MOD
    count3 = count2 * count % MOD

    sumOddValues = count2
    sumOddSquares = (4 * count3 - count) * INVERSE_THREE % MOD

    return (sumOddValues + sumOddSquares - 2) % MOD


def pellIndexForPowerOfTen(exponent):
    getcontext().prec = 80
    two = Decimal(2)
    ten = Decimal(10)
    rootTwo = two.sqrt()
    alpha = Decimal(3) + two * rootTwo
    coefficient = (Decimal(4) + Decimal(3) * rootTwo) / Decimal(4)

    log10Alpha = alpha.ln() / ten.ln()
    log10Coefficient = coefficient.ln() / ten.ln()
    estimate = (Decimal(exponent) - log10Coefficient) / log10Alpha
    index = int(estimate)

    def approximateLog10Perimeter(k):
        return log10Coefficient + Decimal(k) * log10Alpha

    while index > 0 and approximateLog10Perimeter(index) >= exponent:
        index -= 1
    while approximateLog10Perimeter(index + 1) < exponent:
        index += 1

    return max(index, 0)


def multiplyMatrices(left, right):
    rows = len(left)
    inner = len(left[0])
    columns = len(right[0])
    product = [[0] * columns for _ in range(rows)]

    for i in range(rows):
        for k in range(inner):
            value = left[i][k]
            if value == 0:
                continue
            for j in range(columns):
                product[i][j] = (product[i][j] + value * right[k][j]) % MOD

    return product


def matrixPower(matrix, exponent):
    size = len(matrix)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        result[i][i] = 1

    base = [row[:] for row in matrix]
    while exponent:
        if exponent % 2 == 1:
            result = multiplyMatrices(result, base)
        base = multiplyMatrices(base, base)
        exponent //= 2

    return result


def sumLegLegFamily(count):
    if count <= 0:
        return 0
    if count == 1:
        return 12

    transition = [
        [6, MOD - 1, 0],
        [1, 0, 0],
        [6, MOD - 1, 1],
    ]
    initial = [[12], [2], [12]]

    powered = matrixPower(transition, count - 1)
    finalState = multiplyMatrices(powered, initial)
    return finalState[2][0]


def bruteS(limit):
    total = 0

    t = 3
    while True:
        perimeter = t * (t + 1)
        if perimeter > limit:
            break
        total += perimeter
        t += 2

    previous = 2
    current = 12
    while current <= limit:
        total += current
        previous, current = current, 6 * current - previous

    if limit >= 12:
        total -= 12

    return total


def solveForPowerOfTen(exponent):
    legHypotenuseSum = sumLegHypotenuseFamilyForPowerOfTen(exponent)
    pellCount = pellIndexForPowerOfTen(exponent)
    legLegSum = sumLegLegFamily(pellCount)
    return (legHypotenuseSum + legLegSum - 12) % MOD


def runTests():
    assert bruteS(100) == 258
    assert bruteS(10_000) == 172_004


def solve():
    return solveForPowerOfTen(10**10)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
