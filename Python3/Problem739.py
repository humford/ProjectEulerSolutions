import time


MODULUS = 1_000_000_007
INVERSE_TWO = (MODULUS + 1) // 2
INVERSE_BLOCK_SIZE = 200_000


def consecutiveInverses(start, count):
    products = [1] * (count + 1)
    value = start
    for index in range(count):
        products[index + 1] = (products[index] * value) % MODULUS
        value += 1

    inverseProduct = pow(products[count], MODULUS - 2, MODULUS)
    inverses = [0] * count
    value = start + count - 1
    for index in range(count - 1, -1, -1):
        inverses[index] = inverseProduct * products[index] % MODULUS * INVERSE_TWO % MODULUS
        inverseProduct = inverseProduct * value % MODULUS
        value -= 1

    return inverses


def summationProcessValue(sequence):
    row = list(sequence)
    while len(row) > 1:
        row = row[1:]
        total = 0
        nextRow = []
        for value in row:
            total += value
            nextRow.append(total)
        row = nextRow
    return row[0]


def lucasSequence(length):
    if length <= 0:
        return []
    values = [1]
    if length > 1:
        values.append(3)
    while len(values) < length:
        values.append(values[-1] + values[-2])
    return values


def lucasSummationValue(length):
    if length <= 0:
        raise ValueError("length must be positive")

    coefficientIndex = length - 1
    if coefficientIndex == 0:
        return 1
    if coefficientIndex == 1:
        return 3
    if coefficientIndex == 2:
        return 7
    if coefficientIndex == 3:
        return 21

    a0, a1, a2, a3 = 1, 3, 7, 21
    coefficient0, coefficient1, coefficient2, coefficient3 = 2, 26, 62, 50
    denominatorStart = 4
    remaining = coefficientIndex - 3

    while remaining:
        blockLength = min(INVERSE_BLOCK_SIZE, remaining)
        inverses = consecutiveInverses(denominatorStart, blockLength)

        for inverseDenominator in inverses:
            nextValue = (
                coefficient3 * a3
                - coefficient0 * a0
                - coefficient1 * a1
                - coefficient2 * a2
            ) % MODULUS
            nextValue = nextValue * inverseDenominator % MODULUS

            a0, a1, a2, a3 = a1, a2, a3, nextValue
            coefficient0 += 4
            coefficient1 += 23
            coefficient2 += 22
            coefficient3 += 15
            denominatorStart += 1

        remaining -= blockLength

    return a3


def runTests():
    assert summationProcessValue([1] * 8) == 429
    assert summationProcessValue(lucasSequence(8)) == 2_663
    assert lucasSummationValue(8) == 2_663
    assert lucasSummationValue(20) == 742_296_999


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lucasSummationValue(10**8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
