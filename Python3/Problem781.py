import time


MOD = 1_000_000_007

NTT_PRIMES = (
    (998_244_353, 3),
    (1_004_535_809, 3),
    (469_762_049, 3),
)

P1, _ = NTT_PRIMES[0]
P2, _ = NTT_PRIMES[1]
P3, _ = NTT_PRIMES[2]

INV_P1_MOD_P2 = pow(P1, -1, P2)
P12_MOD_P3 = (P1 * P2) % P3
INV_P12_MOD_P3 = pow(P12_MOD_P3, -1, P3)
P1_MOD_P3 = P1 % P3
P1_MOD_MOD = P1 % MOD
P12_MOD_MOD = (P1_MOD_MOD * (P2 % MOD)) % MOD

BIT_REVERSE_CACHE = {}


def bitReversePermutation(length):
    result = [0] * length
    bits = length.bit_length() - 1
    for index in range(length):
        value = index
        reverse = 0
        for _ in range(bits):
            reverse = (reverse << 1) | (value & 1)
            value >>= 1
        result[index] = reverse
    return result


def ntt(values, invert, modulus, root):
    length = len(values)
    reverse = BIT_REVERSE_CACHE.get(length)
    if reverse is None:
        reverse = bitReversePermutation(length)
        BIT_REVERSE_CACHE[length] = reverse

    for i in range(length):
        j = reverse[i]
        if i < j:
            values[i], values[j] = values[j], values[i]

    blockLength = 2
    while blockLength <= length:
        rootStep = pow(root, (modulus - 1) // blockLength, modulus)
        if invert:
            rootStep = pow(rootStep, modulus - 2, modulus)

        half = blockLength // 2
        for start in range(0, length, blockLength):
            multiplier = 1
            for offset in range(half):
                even = values[start + offset]
                odd = values[start + offset + half] * multiplier % modulus

                values[start + offset] = (even + odd) % modulus
                values[start + offset + half] = (even - odd) % modulus
                multiplier = multiplier * rootStep % modulus

        blockLength *= 2

    if invert:
        inverseLength = pow(length, modulus - 2, modulus)
        for i in range(length):
            values[i] = values[i] * inverseLength % modulus


def convolutionPrime(left, right, modulus, root):
    if not left or not right:
        return []

    needed = len(left) + len(right) - 1
    length = 1
    while length < needed:
        length *= 2

    leftValues = left[:] + [0] * (length - len(left))
    rightValues = right[:] + [0] * (length - len(right))
    ntt(leftValues, False, modulus, root)
    ntt(rightValues, False, modulus, root)

    for i in range(length):
        leftValues[i] = leftValues[i] * rightValues[i] % modulus

    ntt(leftValues, True, modulus, root)
    return leftValues[:needed]


def crt3ToMod(r1, r2, r3):
    t2 = (r2 - r1 % P2) * INV_P1_MOD_P2 % P2
    x12ModP3 = (r1 + P1_MOD_P3 * t2) % P3
    t3 = (r3 - x12ModP3) * INV_P12_MOD_P3 % P3

    return (r1 % MOD + P1_MOD_MOD * (t2 % MOD) + P12_MOD_MOD * (t3 % MOD)) % MOD


def reduceForP3(value):
    if value >= P3:
        value -= P3
        if value >= P3:
            value -= P3
    return value


def polynomialMultiply(left, right, limit):
    if not left or not right:
        return []

    needed = min(limit, len(left) + len(right) - 1)
    left = left[: min(len(left), needed)]
    right = right[: min(len(right), needed)]

    left1 = [value if value < P1 else value - P1 for value in left]
    right1 = [value if value < P1 else value - P1 for value in right]
    left2 = left[:]
    right2 = right[:]
    left3 = [reduceForP3(value) for value in left]
    right3 = [reduceForP3(value) for value in right]

    result1 = convolutionPrime(left1, right1, *NTT_PRIMES[0])
    result2 = convolutionPrime(left2, right2, *NTT_PRIMES[1])
    result3 = convolutionPrime(left3, right3, *NTT_PRIMES[2])

    return [crt3ToMod(result1[i], result2[i], result3[i]) for i in range(needed)]


def polynomialInverse(poly, length):
    inverse = [pow(poly[0], MOD - 2, MOD)]
    currentLength = 1

    while currentLength < length:
        nextLength = min(2 * currentLength, length)
        product = polynomialMultiply(poly[:nextLength], inverse, nextLength)

        correction = [0] * nextLength
        correction[0] = (2 - product[0]) % MOD
        for i in range(1, nextLength):
            correction[i] = (-product[i]) % MOD

        inverse = polynomialMultiply(inverse, correction, nextLength)
        currentLength = nextLength

    return inverse


def buildSeries(maxM):
    degree = 2 * maxM

    factorial = [1] * (degree + 1)
    for n in range(1, degree + 1):
        factorial[n] = factorial[n - 1] * n % MOD

    inverseFactorial = [1] * (degree + 1)
    inverseFactorial[degree] = pow(factorial[degree], MOD - 2, MOD)
    for n in range(degree, 0, -1):
        inverseFactorial[n - 1] = inverseFactorial[n] * n % MOD

    alternatingExpPrefix = [0] * (degree + 1)
    total = 0
    for n in range(degree + 1):
        term = inverseFactorial[n]
        if n % 2:
            term = MOD - term
        total = (total + term) % MOD
        alternatingExpPrefix[n] = total

    A = [0] * (maxM + 1)
    B = [0] * (maxM + 1)
    doubleFactorial = 1

    for m in range(maxM + 1):
        if m > 0:
            doubleFactorial = doubleFactorial * (2 * m - 1) % MOD

        s2m = alternatingExpPrefix[2 * m]
        s2mMinus1 = alternatingExpPrefix[2 * m - 1] if m > 0 else 0

        A[m] = doubleFactorial * s2m % MOD
        B[m] = doubleFactorial * ((2 * m + 1) * s2m + s2mMinus1) % MOD

    return A, B


def connectedDiagramCounts(maxN):
    maxM = maxN // 2
    A, B = buildSeries(maxM)
    inverseA = polynomialInverse(A, maxM + 1)
    return polynomialMultiply(B, inverseA, maxM + 1)


def F(n):
    if n % 2:
        return 0
    return connectedDiagramCounts(n)[n // 2]


def runTests(counts):
    assert counts[2] == 5
    assert counts[4] == 319


if __name__ == "__main__":
    start = time.time()
    counts = connectedDiagramCounts(50_000)
    runTests(counts)
    answer = counts[25_000]
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
