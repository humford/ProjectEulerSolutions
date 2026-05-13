import time


MODULUS = 1_000_000_007
TARGET_M = 8
TARGET_W = 64
XOR_SIZE = 64


def fastWalshHadamard(values, inverse=False):
    step = 1
    while step < len(values):
        jump = 2 * step
        for start in range(0, len(values), jump):
            for index in range(start, start + step):
                left = values[index]
                right = values[index + step]
                values[index] = (left + right) % MODULUS
                values[index + step] = (left - right) % MODULUS
        step = jump

    if inverse:
        inverseLength = pow(len(values), MODULUS - 2, MODULUS)
        for index in range(len(values)):
            values[index] = values[index] * inverseLength % MODULUS


def multiplyPolynomials(left, right):
    leftCoeffs, leftOffset = left
    rightCoeffs, rightOffset = right

    if len(leftCoeffs) < len(rightCoeffs):
        leftCoeffs, rightCoeffs = rightCoeffs, leftCoeffs
        leftOffset, rightOffset = rightOffset, leftOffset

    result = [0] * (len(leftCoeffs) + len(rightCoeffs) - 1)
    for i, leftCoeff in enumerate(leftCoeffs):
        if leftCoeff == 0:
            continue
        for j, rightCoeff in enumerate(rightCoeffs):
            if rightCoeff:
                result[i + j] = (result[i + j] + leftCoeff * rightCoeff) % MODULUS

    return result, leftOffset + rightOffset


def powerPolynomial(polynomial, exponent):
    result = ([1], 0)
    base = polynomial

    while exponent:
        if exponent % 2 == 1:
            result = multiplyPolynomials(result, base)
        exponent //= 2
        if exponent:
            base = multiplyPolynomials(base, base)

    return result


def staircaseCounts(w):
    maxDifference = w - 2
    counts = [[0] * XOR_SIZE for _ in range(2 * maxDifference + 1)]

    for k in range(1, w - 1):
        limit = w - k
        nimber = k - 1
        maxAbsDifference = limit - 2

        for difference in range(maxAbsDifference + 1):
            count = (limit - difference) // 2
            if count == 0:
                continue

            counts[maxDifference + difference][nimber] = (
                counts[maxDifference + difference][nimber] + count
            ) % MODULUS
            if difference != 0:
                counts[maxDifference - difference][nimber] = (
                    counts[maxDifference - difference][nimber] + count
                ) % MODULUS

    return counts, maxDifference


def R(m, w):
    # An (a,b,k)-staircase in the "move any number of squares" game has
    # value (b-a) + *(k-1).  A sum is winning for Right iff its integer part
    # is positive, or the integer part is zero and the nimber xor is nonzero.
    counts, maxDifference = staircaseCounts(w)

    transformed = []
    for valuesByNimber in counts:
        transformedValues = valuesByNimber[:]
        fastWalshHadamard(transformedValues)
        transformed.append(transformedValues)

    finalOffset = m * maxDifference
    finalLength = 2 * finalOffset + 1
    transformedPowers = [[0] * finalLength for _ in range(XOR_SIZE)]

    for xorIndex in range(XOR_SIZE):
        coefficients = [transformed[d][xorIndex] for d in range(len(transformed))]
        powered, offset = powerPolynomial((coefficients, maxDifference), m)
        if offset != finalOffset:
            raise ValueError("unexpected polynomial offset")
        transformedPowers[xorIndex][:len(powered)] = powered

    answer = 0
    for degree in range(finalLength):
        valuesByTransform = [transformedPowers[xorIndex][degree] for xorIndex in range(XOR_SIZE)]
        fastWalshHadamard(valuesByTransform, inverse=True)
        totalDifference = degree - finalOffset

        if totalDifference > 0:
            answer = (answer + sum(valuesByTransform)) % MODULUS
        elif totalDifference == 0:
            answer = (answer + sum(valuesByTransform[1:])) % MODULUS

    return answer


def solve():
    return R(TARGET_M, TARGET_W)


def runTests():
    assert R(2, 4) == 7
    assert R(3, 9) == 314_104
    assert solve() == 858_945_298


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
