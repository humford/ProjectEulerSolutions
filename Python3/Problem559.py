import math
import time

import numpy as np


MODULUS = 1_000_000_123
CONVOLUTION_BASE = 1 << 15
DIRECT_RECURRENCE_LIMIT = 250


def convolutionMod(left, right, modulus=MODULUS):
    if not left or not right:
        return []

    length = len(left) + len(right) - 1
    size = 1 << (length - 1).bit_length()

    leftArray = np.array(left, dtype=np.int64)
    rightArray = np.array(right, dtype=np.int64)

    leftLow = leftArray % CONVOLUTION_BASE
    leftHigh = leftArray // CONVOLUTION_BASE
    rightLow = rightArray % CONVOLUTION_BASE
    rightHigh = rightArray // CONVOLUTION_BASE

    leftLowFft = np.fft.rfft(leftLow, size)
    leftHighFft = np.fft.rfft(leftHigh, size)
    rightLowFft = np.fft.rfft(rightLow, size)
    rightHighFft = np.fft.rfft(rightHigh, size)

    low = np.rint(np.fft.irfft(leftLowFft * rightLowFft, size)[:length]).astype(
        np.int64
    )
    high = np.rint(
        np.fft.irfft(leftHighFft * rightHighFft, size)[:length]
    ).astype(np.int64)
    middle = np.rint(
        np.fft.irfft(
            (leftLowFft + leftHighFft) * (rightLowFft + rightHighFft),
            size,
        )[:length]
    ).astype(np.int64)
    cross = middle - low - high

    base = CONVOLUTION_BASE % modulus
    baseSquared = (base * base) % modulus
    result = (low % modulus + base * (cross % modulus) + baseSquared * (high % modulus)) % modulus
    return result.astype(np.int64).tolist()


def inverseSeries(series, length):
    inverse = [pow(series[0], -1, MODULUS)]
    while len(inverse) < length:
        size = min(2 * len(inverse), length)
        product = convolutionMod(series[:size], inverse)[:size]
        correction = [0] * size
        correction[0] = (2 - product[0]) % MODULUS
        for index in range(1, size):
            correction[index] = (-product[index]) % MODULUS
        inverse = convolutionMod(inverse, correction)[:size]
    return inverse


def factorialTables(n, modulus=MODULUS):
    factorials = [1] * (n + 1)
    inverseFactorials = [1] * (n + 1)
    for value in range(1, n + 1):
        factorials[value] = factorials[value - 1] * value % modulus

    inverseFactorials[n] = pow(factorials[n], -1, modulus)
    for value in range(n, 0, -1):
        inverseFactorials[value - 1] = inverseFactorials[value] * value % modulus

    return factorials, inverseFactorials


def coefficientWeights(n, exponent, modulus=MODULUS):
    factorials, inverseFactorials = factorialTables(n, modulus)
    weights = [pow(value, exponent, modulus) for value in inverseFactorials]
    scale = pow(factorials[n], exponent, modulus)
    return weights, scale


def denominatorForBlocks(k, n, weights):
    blockCount = n // k
    denominator = [1] * (blockCount + 1)
    for count in range(1, blockCount + 1):
        value = weights[count * k]
        denominator[count] = (-value if count % 2 else value) % MODULUS
    return denominator


def inverseDenominator(denominator):
    degree = len(denominator) - 1
    if degree <= DIRECT_RECURRENCE_LIMIT:
        inverse = [0] * (degree + 1)
        inverse[0] = 1
        for index in range(1, degree + 1):
            total = 0
            for step in range(1, index + 1):
                total += denominator[step] * inverse[index - step]
            inverse[index] = (-total) % MODULUS
        return inverse

    return inverseSeries(denominator, degree + 1)


def coefficientSum(k, n, weights):
    blockCount, tail = divmod(n, k)
    blockInverse = inverseDenominator(denominatorForBlocks(k, n, weights))

    if tail == 0:
        return blockInverse[blockCount]

    total = 0
    for mergedBlocks in range(blockCount + 1):
        term = weights[mergedBlocks * k + tail] * blockInverse[
            blockCount - mergedBlocks
        ]
        total += -term if mergedBlocks % 2 else term
    return total % MODULUS


def permutedMatrixCount(k, r, n):
    weights, scale = coefficientWeights(n, r)
    return scale * coefficientSum(k, n, weights) % MODULUS


def permutedMatrixSum(n):
    weights, scale = coefficientWeights(n, n)
    total = 0
    for k in range(1, n + 1):
        total += coefficientSum(k, n, weights)
    return scale * (total % MODULUS) % MODULUS


def permutedMatrixCountBrute(k, r, n):
    fullBlocks, tail = divmod(n, k)
    pieces = [k] * fullBlocks + ([tail] if tail else [])
    boundaryCount = len(pieces) - 1
    factorial = math.factorial(n)
    total = 0

    for selected in range(1 << boundaryCount):
        segmentLengths = []
        current = pieces[0]
        for boundary in range(boundaryCount):
            if selected & (1 << boundary):
                segmentLengths.append(current)
                current = pieces[boundary + 1]
            else:
                current += pieces[boundary + 1]
        segmentLengths.append(current)

        denominator = 1
        for length in segmentLengths:
            denominator *= math.factorial(length)
        rowCount = factorial // denominator
        sign = -1 if (boundaryCount - selected.bit_count()) % 2 else 1
        total += sign * rowCount**r

    return total


def permutedMatrixSumBrute(n):
    return sum(permutedMatrixCountBrute(k, n, n) for k in range(1, n + 1))


def runTests():
    assert permutedMatrixCountBrute(1, 2, 3) == 19
    assert permutedMatrixCount(1, 2, 3) == 19
    assert permutedMatrixCount(2, 4, 6) == 65_508_751
    assert permutedMatrixCount(7, 5, 30) == 161_858_102
    assert permutedMatrixSumBrute(5) == 21_879_393_751
    assert permutedMatrixSum(5) == 21_879_393_751 % MODULUS
    assert permutedMatrixSum(50) == 819_573_537


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = permutedMatrixSum(50_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
