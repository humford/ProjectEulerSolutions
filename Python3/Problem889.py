from math import comb
import time


MODULUS = 1_000_062_031
TARGET_K = 10**18 + 31
TARGET_T = 10**14 + 31
TARGET_R = 62


def setBitPositions(number):
    while number:
        bit = number & -number
        yield bit.bit_length() - 1
        number -= bit


def numeratorBitPositions(t, r):
    maxCoefficientBits = comb(r, r // 2).bit_length()
    if t <= maxCoefficientBits:
        raise ValueError("binomial blocks overlap")

    positions = []
    for exponent in range(r + 1):
        coefficient = comb(r, exponent)
        base = t * exponent
        for bit in setBitPositions(coefficient):
            positions.append(base + bit)

    positions.sort()
    for index in range(1, len(positions)):
        assert positions[index] != positions[index - 1]

    return positions


def bruteFMod(k, t, r, modulus):
    denominator = (1 << k) + 1
    numerator = pow((1 << t) + 1, r, denominator)
    inverseTwo = pow(2, -1, modulus)

    value = numerator
    weight = pow(2, k, modulus)
    total = 0

    for _ in range(k):
        distance = min(value, denominator - value)
        total = (total + distance % modulus * weight) % modulus
        value = (2 * value) % denominator
        weight = weight * inverseTwo % modulus

    return total


def fastFMod(k, t, r, modulus):
    positions = numeratorBitPositions(t, r)
    if positions[-1] >= k:
        raise ValueError("fast path requires numerator smaller than 2^k")

    powerK = pow(2, k, modulus)
    lowPowers = [pow(2, position, modulus) for position in positions]
    highPowers = [powerK * value % modulus for value in lowPowers]

    prefixLow = [0]
    prefixHigh = [0]
    for low, high in zip(lowPowers, highPowers):
        prefixLow.append((prefixLow[-1] + low) % modulus)
        prefixHigh.append((prefixHigh[-1] + high) % modulus)

    totalLow = prefixLow[-1]
    total = 0

    for position, low, high in zip(positions, lowPowers, highPowers):
        total += ((k - position) % modulus) * high
        total -= (position % modulus) * low
        total %= modulus

    for index in range(1, len(positions)):
        position = positions[index]

        signedShift = (
            prefixHigh[index + 1]
            - (totalLow - prefixLow[index + 1])
        ) % modulus
        scale = 2 * lowPowers[index] % modulus
        denominatorScaled = (powerK * scale + scale) % modulus

        total += denominatorScaled - 2 * signedShift
        total %= modulus

    return total


def FMod(k, t, r, modulus=MODULUS):
    if k <= 1500 and t <= 2000:
        return bruteFMod(k, t, r, modulus)
    return fastFMod(k, t, r, modulus)


def solve():
    return FMod(TARGET_K, TARGET_T, TARGET_R)


def runTests():
    assert FMod(3, 1, 1) == 42
    assert FMod(13, 3, 3) == 23093880
    assert FMod(103, 13, 6) == 878922518


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 424315113
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
