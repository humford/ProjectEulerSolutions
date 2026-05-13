import time


TARGET_M = 9898
MODULUS = 989_898_989


def modInverse(value, modulus):
    oldR, r = value, modulus
    oldS, s = 1, 0

    while r:
        quotient = oldR // r
        oldR, r = r, oldR - quotient * r
        oldS, s = s, oldS - quotient * s

    if oldR != 1:
        raise ValueError("inverse does not exist")

    return oldS % modulus


def ceilDiv(numerator, denominator):
    return -((-numerator) // denominator)


def triangular(S):
    if S < 0:
        return 0
    return (S + 2) * (S + 1) // 2


def boundedSumCount(lengths, target):
    total = 0

    for mask in range(8):
        shifted = target
        sign = 1
        for index, length in enumerate(lengths):
            if mask & (1 << index):
                shifted -= length
                sign = -sign
        total += sign * triangular(shifted)

    return total


def GExact(m):
    allMonochrome = 3 * m * (m - 1)

    twoMixed = 0
    for t in range(1, m):
        remaining = m - t
        twoMixed += (1 << (t - 1)) * remaining * (remaining - 1)
    twoMixed *= 6

    threeMixed = 0
    carryZero = [1]
    carryOne = [1]

    for u in range(1, m - 1):
        for T in range(u + 1, m):
            lowerFreeBits = T - u - 1
            lowFactor = 1 << lowerFreeBits

            for fractionalSum, finalCarry in ((1, 0), (2, 1)):
                for shortPlacement in range(3):
                    exponents = [T, T, T]
                    exponents[shortPlacement] = u

                    for signMask in range(8):
                        negativeCount = signMask.bit_count()
                        weightTarget = fractionalSum - negativeCount
                        numerator = weightTarget + u + 1 - 4 * finalCarry
                        if numerator % 2:
                            continue

                        carryCount = numerator // 2
                        if not 0 <= carryCount <= u - 1:
                            continue

                        numeratorWays = (
                            carryZero[carryCount]
                            if finalCarry == 0
                            else carryOne[carryCount]
                        )

                        starts = []
                        lengths = []
                        for index, exponent in enumerate(exponents):
                            length = m - exponent
                            lengths.append(length)
                            if signMask & (1 << index):
                                starts.append(-length)
                            else:
                                starts.append(0)

                        baseTarget = -fractionalSum - sum(starts)
                        baseWays = boundedSumCount(lengths, baseTarget)
                        threeMixed += numeratorWays * lowFactor * baseWays

        nextZero = [0] * (u + 1)
        nextOne = [0] * (u + 1)
        nextZero[0] = 3 * carryZero[0]
        nextOne[0] = carryZero[0]
        for count in range(1, u):
            nextZero[count] = 3 * carryZero[count] + carryOne[count - 1]
            nextOne[count] = carryZero[count] + 3 * carryOne[count - 1]
        nextZero[u] = carryOne[u - 1]
        nextOne[u] = 3 * carryOne[u - 1]
        carryZero, carryOne = nextZero, nextOne

    return allMonochrome + twoMixed + threeMixed


def inversePowerPrefixTables(m, modulus):
    inverseTwo = modInverse(2, modulus)
    inversePowers = [1] * (m + 1)
    for index in range(1, m + 1):
        inversePowers[index] = inversePowers[index - 1] * inverseTwo % modulus

    prefix0 = [0] * (m + 1)
    prefix1 = [0] * (m + 1)
    prefix2 = [0] * (m + 1)
    for index in range(1, m + 1):
        weight = inversePowers[index]
        prefix0[index] = (prefix0[index - 1] + weight) % modulus
        prefix1[index] = (prefix1[index - 1] + index * weight) % modulus
        prefix2[index] = (prefix2[index - 1] + index * index * weight) % modulus

    return inversePowers, prefix0, prefix1, prefix2


def intervalSums(prefix0, prefix1, prefix2, left, right, modulus):
    if left > right:
        return 0, 0, 0

    return (
        (prefix0[right] - prefix0[left - 1]) % modulus,
        (prefix1[right] - prefix1[left - 1]) % modulus,
        (prefix2[right] - prefix2[left - 1]) % modulus,
    )


def GMod(m, modulus):
    inverseTwo = modInverse(2, modulus)

    powersOfTwo = [1] * (m + 1)
    for index in range(1, m + 1):
        powersOfTwo[index] = 2 * powersOfTwo[index - 1] % modulus

    _, prefix0, prefix1, prefix2 = inversePowerPrefixTables(m, modulus)

    def sumQuadratic(alpha, beta, left, right):
        if left > right:
            return 0

        s0, s1, s2 = intervalSums(
            prefix0, prefix1, prefix2, left, right, modulus
        )
        alpha %= modulus
        beta %= modulus
        term2 = alpha * alpha % modulus
        term1 = alpha * (2 * beta + 3) % modulus
        term0 = (beta * beta + 3 * beta + 2) % modulus
        return (term2 * s2 + term1 * s1 + term0 * s0) * inverseTwo % modulus

    def sumBaseForParameters(b, fractionalSum, p, q):
        total = 0
        upper = b - 1

        for countA, multiplicity in ((0, 1), (1, 2), (2, 1)):
            for countB in (0, 1):
                sign = -1 if (countA + countB) % 2 else 1
                alpha = p - countA
                beta = (q - countB) * b - fractionalSum

                if alpha == 0:
                    if beta < 0:
                        continue
                    left, right = 1, upper
                elif alpha > 0:
                    left, right = max(1, ceilDiv(-beta, alpha)), upper
                else:
                    left, right = 1, min(upper, beta // (-alpha))

                if left <= right:
                    total += sign * multiplicity * sumQuadratic(alpha, beta, left, right)
                    total %= modulus

        return total

    def baseWeights(b, fractionalSum):
        baseByNegatives = [0, 0, 0, 0]
        sums = [
            [
                sumBaseForParameters(b, fractionalSum, p, q)
                for q in (0, 1)
            ]
            for p in (0, 1, 2)
        ]

        for negatives in range(4):
            total = 0
            for bIsNegative in (0, 1):
                aNegatives = negatives - bIsNegative
                if not 0 <= aNegatives <= 2:
                    continue
                multiplicity = 3 * (1 if aNegatives != 1 else 2)
                total += multiplicity * sums[aNegatives][bIsNegative]
            baseByNegatives[negatives] = total * powersOfTwo[b - 1] % modulus

        return baseByNegatives

    allMonochrome = 3 * m * (m - 1) % modulus

    twoMixed = 0
    for t in range(1, m):
        remaining = m - t
        twoMixed += powersOfTwo[t - 1] * remaining * (remaining - 1)
        twoMixed %= modulus
    twoMixed = 6 * twoMixed % modulus

    threeMixed = 0
    carryZero = [1]
    carryOne = [1]

    for u in range(1, m - 1):
        b = m - u
        baseForOne = baseWeights(b, 1)
        baseForTwo = baseWeights(b, 2)

        for fractionalSum, finalCarry, base in (
            (1, 0, baseForOne),
            (2, 1, baseForTwo),
        ):
            for negatives in (1, 2, 3):
                weightTarget = fractionalSum - negatives
                numerator = weightTarget + u + 1 - 4 * finalCarry
                if numerator % 2:
                    continue

                carryCount = numerator // 2
                if not 0 <= carryCount <= u - 1:
                    continue

                numeratorWays = (
                    carryZero[carryCount]
                    if finalCarry == 0
                    else carryOne[carryCount]
                )
                threeMixed += numeratorWays * base[negatives]
                threeMixed %= modulus

        nextZero = [0] * (u + 1)
        nextOne = [0] * (u + 1)
        nextZero[0] = 3 * carryZero[0] % modulus
        nextOne[0] = carryZero[0] % modulus
        for count in range(1, u):
            nextZero[count] = (3 * carryZero[count] + carryOne[count - 1]) % modulus
            nextOne[count] = (carryZero[count] + 3 * carryOne[count - 1]) % modulus
        nextZero[u] = carryOne[u - 1] % modulus
        nextOne[u] = 3 * carryOne[u - 1] % modulus
        carryZero, carryOne = nextZero, nextOne

    return (allMonochrome + twoMixed + threeMixed) % modulus


def solve():
    return GMod(TARGET_M, MODULUS)


def runTests():
    assert GExact(2) == 6
    assert GExact(5) == 348
    assert GExact(20) == 125825982708
    assert GMod(20, MODULUS) == 125825982708 % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 670785433
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
