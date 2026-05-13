import itertools
import math
import time

import numpy as np


MODULUS = 1_000_000_007


def bruteGrundyValues(limit):
    grundy = [0] * (limit + 1)
    for stones in range(1, limit + 1):
        reachable = {
            grundy[stones - remove]
            for remove in range(1, stones + 1)
            if math.gcd(remove, stones) == 1
        }
        mex = 0
        while mex in reachable:
            mex += 1
        grundy[stones] = mex
    return grundy


def grundyDistribution(n):
    limit = n - 1
    counts = [0, 0]
    counts[0] = limit // 2
    if limit >= 1:
        counts[1] = 1

    marked = bytearray(n)
    primeIndex = 1
    for prime in range(3, n, 2):
        if marked[prime]:
            continue

        primeIndex += 1
        count = 0
        for multiple in range(prime, n, 2 * prime):
            if not marked[multiple]:
                marked[multiple] = 1
                count += 1

        while len(counts) <= primeIndex:
            counts.append(0)
        counts[primeIndex] = count

    size = 1 << max(1, (len(counts) - 1).bit_length())
    distribution = np.zeros(size, dtype=np.int64)
    distribution[: len(counts)] = counts
    return distribution


def xorWalshTransform(values, modulus=MODULUS):
    half = 1
    length = len(values)
    while half < length:
        blocks = values.reshape(-1, 2 * half)
        left = blocks[:, :half].copy()
        right = blocks[:, half:].copy()
        blocks[:, :half] = (left + right) % modulus
        blocks[:, half:] = (left - right) % modulus
        half *= 2


def arrayPower(values, exponent, modulus=MODULUS):
    result = np.ones_like(values)
    base = values.copy()
    while exponent:
        if exponent & 1:
            result = (result * base) % modulus
        exponent //= 2
        if exponent:
            base = (base * base) % modulus
    return result


def losingPositionCount(n, k):
    distribution = grundyDistribution(n)
    xorWalshTransform(distribution)
    powered = arrayPower(distribution, k)
    xorWalshTransform(powered)
    inverseLength = pow(len(powered), -1, MODULUS)
    return int(powered[0] * inverseLength % MODULUS)


def losingPositionCountBrute(n, k):
    grundy = bruteGrundyValues(n - 1)
    total = 0
    for piles in itertools.product(range(1, n), repeat=k):
        xorValue = 0
        for pile in piles:
            xorValue ^= grundy[pile]
        if xorValue == 0:
            total += 1
    return total


def runTests():
    brute = bruteGrundyValues(80)
    for stones in range(1, 81):
        if stones == 1:
            expected = 1
        elif stones % 2 == 0:
            expected = 0
        else:
            primeIndex = 1
            for candidate in range(3, stones + 1, 2):
                isPrime = all(
                    candidate % divisor
                    for divisor in range(3, math.isqrt(candidate) + 1, 2)
                )
                if isPrime:
                    primeIndex += 1
                    if stones % candidate == 0:
                        break
            expected = primeIndex
        assert brute[stones] == expected

    assert losingPositionCountBrute(5, 2) == 6
    assert losingPositionCount(5, 2) == 6
    assert losingPositionCount(10, 5) == 9_964
    assert losingPositionCount(10, 10) == 472_400_303
    assert losingPositionCount(10 ** 3, 10 ** 3) == 954_021_836


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = losingPositionCount(10 ** 7, 10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
