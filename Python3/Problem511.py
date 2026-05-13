import time


MODULUS = 10**9
NTT_PRIMES = (998_244_353, 1_004_535_809, 469_762_049)
NTT_ROOTS = (3, 3, 3)


def divisors(n):
    factors = []
    candidate = 2

    while candidate * candidate <= n:
        if n % candidate == 0:
            exponent = 0
            while n % candidate == 0:
                n //= candidate
                exponent += 1
            factors.append((candidate, exponent))

        candidate += 1 if candidate == 2 else 2

    if n > 1:
        factors.append((n, 1))

    result = [1]
    for prime, exponent in factors:
        result = [divisor * primePower for divisor in result for primePower in powers(prime, exponent)]

    return result


def powers(base, exponent):
    value = 1
    result = []

    for _ in range(exponent + 1):
        result.append(value)
        value *= base

    return result


def ntt(values, modulus, root, invert):
    length = len(values)
    swapIndex = 0

    for index in range(1, length):
        bit = length >> 1
        while swapIndex & bit:
            swapIndex ^= bit
            bit >>= 1
        swapIndex ^= bit

        if index < swapIndex:
            values[index], values[swapIndex] = values[swapIndex], values[index]

    blockLength = 2
    while blockLength <= length:
        rootStep = pow(root, (modulus - 1) // blockLength, modulus)
        if invert:
            rootStep = pow(rootStep, modulus - 2, modulus)

        halfLength = blockLength // 2
        for start in range(0, length, blockLength):
            factor = 1
            for offset in range(start, start + halfLength):
                left = values[offset]
                right = values[offset + halfLength] * factor % modulus
                values[offset] = (left + right) % modulus
                values[offset + halfLength] = (left - right) % modulus
                factor = factor * rootStep % modulus

        blockLength *= 2

    if invert:
        inverseLength = pow(length, modulus - 2, modulus)
        for index in range(length):
            values[index] = values[index] * inverseLength % modulus


def primeCyclicConvolution(left, right, cycleLength, modulus, root):
    transformLength = 1
    while transformLength < 2 * cycleLength - 1:
        transformLength *= 2

    leftValues = [value % modulus for value in left] + [0] * (transformLength - cycleLength)
    rightValues = [value % modulus for value in right] + [0] * (transformLength - cycleLength)

    ntt(leftValues, modulus, root, False)
    ntt(rightValues, modulus, root, False)

    for index in range(transformLength):
        leftValues[index] = leftValues[index] * rightValues[index] % modulus

    ntt(leftValues, modulus, root, True)

    return [
        (leftValues[index] + (leftValues[index + cycleLength] if index + cycleLength < 2 * cycleLength - 1 else 0))
        % modulus
        for index in range(cycleLength)
    ]


PRIME_1, PRIME_2, PRIME_3 = NTT_PRIMES
PRIME_12 = PRIME_1 * PRIME_2
INVERSE_PRIME_1_MOD_2 = pow(PRIME_1, -1, PRIME_2)
INVERSE_PRIME_12_MOD_3 = pow(PRIME_12 % PRIME_3, -1, PRIME_3)


def cyclicConvolution(left, right):
    cycleLength = len(left)
    residues = [
        primeCyclicConvolution(left, right, cycleLength, modulus, root)
        for modulus, root in zip(NTT_PRIMES, NTT_ROOTS)
    ]
    result = []

    for first, second, third in zip(*residues):
        step = ((second - first) * INVERSE_PRIME_1_MOD_2) % PRIME_2
        value = first + PRIME_1 * step
        step = ((third - value) % PRIME_3) * INVERSE_PRIME_12_MOD_3 % PRIME_3
        value += PRIME_12 * step
        result.append(value % MODULUS)

    return result


def directCyclicConvolution(left, right):
    cycleLength = len(left)
    result = [0] * cycleLength

    for leftIndex, leftValue in enumerate(left):
        if leftValue == 0:
            continue

        for rightIndex, rightValue in enumerate(right):
            if rightValue:
                result[(leftIndex + rightIndex) % cycleLength] = (
                    result[(leftIndex + rightIndex) % cycleLength] + leftValue * rightValue
                ) % MODULUS

    return result


def multiplyResidues(left, right):
    if len(left) <= 128:
        return directCyclicConvolution(left, right)

    return cyclicConvolution(left, right)


def divisorResidues(n, k):
    residues = [0] * k

    for divisor in divisors(n):
        residues[divisor % k] += 1

    return residues


def niceSequenceCount(n, k):
    base = divisorResidues(n, k)
    result = [0] * k
    result[0] = 1
    exponent = n

    while exponent:
        if exponent & 1:
            result = multiplyResidues(result, base)

        exponent //= 2
        if exponent:
            base = multiplyResidues(base, base)

    return result[(-n) % k]


def runTests():
    assert niceSequenceCount(3, 4) == 4
    assert niceSequenceCount(4, 11) == 8
    assert niceSequenceCount(1_111, 24) == 840_643_584


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = niceSequenceCount(1_234_567_898_765, 4_321)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
