import time


MODULUS = 1_111_124_111
TARGET_N = 100_000
NTT_PRIMES = (998_244_353, 1_004_535_809, 469_762_049)
PRIMITIVE_ROOT = 3


def numberTheoreticTransform(values, modulus, invert=False):
    length = len(values)
    j = 0

    for i in range(1, length):
        bit = length >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit

        if i < j:
            values[i], values[j] = values[j], values[i]

    blockLength = 2
    while blockLength <= length:
        root = pow(PRIMITIVE_ROOT, (modulus - 1) // blockLength, modulus)
        if invert:
            root = pow(root, modulus - 2, modulus)

        half = blockLength // 2
        for start in range(0, length, blockLength):
            weight = 1
            for index in range(start, start + half):
                left = values[index]
                right = values[index + half] * weight % modulus
                values[index] = (left + right) % modulus
                values[index + half] = (left - right) % modulus
                weight = weight * root % modulus

        blockLength *= 2

    if invert:
        inverseLength = pow(length, modulus - 2, modulus)
        for index in range(length):
            values[index] = values[index] * inverseLength % modulus


def convolutionPrime(left, right, modulus, limit):
    fullLength = len(left) + len(right) - 1
    resultLength = min(fullLength, limit)
    transformLength = 1

    while transformLength < fullLength:
        transformLength *= 2

    leftValues = [value % modulus for value in left] + [0] * (
        transformLength - len(left)
    )
    rightValues = [value % modulus for value in right] + [0] * (
        transformLength - len(right)
    )

    numberTheoreticTransform(leftValues, modulus)
    numberTheoreticTransform(rightValues, modulus)

    for index in range(transformLength):
        leftValues[index] = leftValues[index] * rightValues[index] % modulus

    numberTheoreticTransform(leftValues, modulus, invert=True)
    return leftValues[:resultLength]


INVERSE_M1_MOD_M2 = pow(NTT_PRIMES[0], -1, NTT_PRIMES[1])
M1_M2 = NTT_PRIMES[0] * NTT_PRIMES[1]
INVERSE_M1_M2_MOD_M3 = pow(M1_M2 % NTT_PRIMES[2], -1, NTT_PRIMES[2])


def convolution(left, right, limit):
    resultLength = min(len(left) + len(right) - 1, limit)
    residues = [
        convolutionPrime(left, right, prime, limit)
        for prime in NTT_PRIMES
    ]
    result = [0] * resultLength
    m1, m2, m3 = NTT_PRIMES

    for index in range(resultLength):
        r1 = residues[0][index]
        r2 = residues[1][index]
        r3 = residues[2][index]
        t2 = ((r2 - r1) % m2) * INVERSE_M1_MOD_M2 % m2
        xModuloM3 = (r1 + (m1 % m3) * t2) % m3
        t3 = ((r3 - xModuloM3) % m3) * INVERSE_M1_M2_MOD_M3 % m3
        result[index] = (
            r1 % MODULUS
            + (m1 % MODULUS) * t2
            + (M1_M2 % MODULUS) * t3
        ) % MODULUS

    return result


def polynomialInverse(polynomial, length):
    inverse = [pow(polynomial[0], -1, MODULUS)]
    currentLength = 1

    while currentLength < length:
        nextLength = min(2 * currentLength, length)
        product = convolution(polynomial[:nextLength], inverse, nextLength)
        correction = [0] * nextLength
        correction[0] = (2 - product[0]) % MODULUS

        for index in range(1, nextLength):
            correction[index] = -product[index] % MODULUS

        inverse = convolution(inverse, correction, nextLength)
        currentLength = nextLength

    return inverse[:length]


def oddRunSeriesCoefficients(limit):
    # For one value a, an odd-length run contributes z + z^3 + z^5 + ...
    # with z = x^a.  Smirnov words for adjacent unequal runs transform this
    # to z / (1 + z - z^2).  Its coefficients are signed Fibonacci numbers.
    runCoefficients = [0] * (limit + 1)
    runCoefficients[1] = 1

    for n in range(2, limit + 1):
        runCoefficients[n] = (
            -runCoefficients[n - 1] + runCoefficients[n - 2]
        ) % MODULUS

    series = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        coefficient = runCoefficients[divisor]
        if coefficient == 0:
            continue

        for multiple in range(divisor, limit + 1, divisor):
            series[multiple] = (series[multiple] + coefficient) % MODULUS

    return series


def F(n):
    coefficients = oddRunSeriesCoefficients(n)
    denominator = [1] + [
        -coefficients[index] % MODULUS
        for index in range(1, n + 1)
    ]

    return polynomialInverse(denominator, n + 1)[n]


def bruteF(n):
    def compositions(total, last=()):
        if total == 0:
            yield last
            return

        for first in range(1, total + 1):
            yield from compositions(total - first, last + (first,))

    def hasOddRuns(composition):
        index = 0
        while index < len(composition):
            end = index
            while end < len(composition) and composition[end] == composition[index]:
                end += 1
            if (end - index) % 2 == 0:
                return False
            index = end
        return True

    return sum(1 for composition in compositions(n) if hasOddRuns(composition))


def solve():
    return F(TARGET_N)


def runTests():
    assert F(5) == 10
    assert [F(n) for n in range(1, 10)] == [
        bruteF(n)
        for n in range(1, 10)
    ]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
