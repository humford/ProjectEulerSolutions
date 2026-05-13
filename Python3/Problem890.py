import time


MODULUS = 1_000_000_007
BASE_BITS = 80
BASE_BYTES = BASE_BITS // 8
TARGET_N = 7**777


def packDigits(values):
    data = bytearray(BASE_BYTES * len(values))

    for index, value in enumerate(values):
        start = BASE_BYTES * index
        data[start:start + BASE_BYTES] = value.to_bytes(BASE_BYTES, "little")

    return int.from_bytes(data, "little")


def convolveAndDecimate(left, right, bit):
    outputLength = len(left) + len(right) - 1
    product = packDigits(left) * packDigits(right)
    productBytes = product.to_bytes(BASE_BYTES * outputLength, "little")

    resultLength = (outputLength - bit + 1) // 2
    result = [0] * resultLength
    for index in range(resultLength):
        source = bit + 2 * index
        start = BASE_BYTES * source
        result[index] = int.from_bytes(
            productBytes[start:start + BASE_BYTES],
            "little",
        ) % MODULUS

    return result


def factorialTables(limit):
    factorials = [1] * (limit + 1)
    inverseFactorials = [1] * (limit + 1)

    for value in range(1, limit + 1):
        factorials[value] = factorials[value - 1] * value % MODULUS

    inverseFactorials[limit] = pow(factorials[limit], MODULUS - 2, MODULUS)
    for value in range(limit, 0, -1):
        inverseFactorials[value - 1] = inverseFactorials[value] * value % MODULUS

    return factorials, inverseFactorials


def binomialRow(top, factorials, inverseFactorials):
    row = [0] * (top + 1)
    topFactorial = factorials[top]

    for selected in range(top + 1):
        row[selected] = (
            topFactorial
            * inverseFactorials[selected]
            * inverseFactorials[top - selected]
        ) % MODULUS

    return row


def coefficientA(exponent):
    if exponent == 0:
        return 1

    bitLength = exponent.bit_length()
    factorials, inverseFactorials = factorialTables(bitLength + 2)
    carryCounts = [1]

    for bitIndex in range(bitLength):
        bit = (exponent >> bitIndex) & 1
        row = binomialRow(bitIndex + 2, factorials, inverseFactorials)
        carryCounts = convolveAndDecimate(carryCounts, row, bit)

    return carryCounts[0]


def pBinaryPartitions(n):
    return coefficientA(n // 2)


def solve():
    return pBinaryPartitions(TARGET_N)


def runTests():
    assert pBinaryPartitions(7) == 6
    assert pBinaryPartitions(7**7) == 144548435


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 820442179
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
