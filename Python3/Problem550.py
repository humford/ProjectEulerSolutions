from math import isqrt
import time


MODULUS = 987_654_321


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"

    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )

    return [number for number in range(limit + 1) if sieve[number]]


def grundyByFactorCount(maxFactorCount):
    grundy = [0] * (maxFactorCount + 1)

    for factorCount in range(2, maxFactorCount + 1):
        reachable = {
            grundy[left] ^ grundy[right]
            for left in range(1, factorCount)
            for right in range(1, factorCount)
        }
        mex = 0
        while mex in reachable:
            mex += 1
        grundy[factorCount] = mex

    return grundy


def grundyDistribution(limit):
    factorCounts = bytearray(limit + 1)

    for prime in primeSieve(limit):
        power = prime
        while power <= limit:
            for multiple in range(power, limit + 1, power):
                factorCounts[multiple] += 1
            if power > limit // prime:
                break
            power *= prime

    countsByFactorCount = [0] * (max(factorCounts) + 1)
    for factorCount in factorCounts[2:]:
        countsByFactorCount[factorCount] += 1

    grundy = grundyByFactorCount(len(countsByFactorCount) - 1)
    distributionSize = 1
    while distributionSize <= max(grundy):
        distributionSize *= 2

    distribution = [0] * distributionSize
    for factorCount, count in enumerate(countsByFactorCount):
        if factorCount:
            distribution[grundy[factorCount]] += count

    return distribution


def xorConvolve(left, right, modulus=None):
    result = [0] * len(left)

    for leftIndex, leftValue in enumerate(left):
        if not leftValue:
            continue
        for rightIndex, rightValue in enumerate(right):
            if rightValue:
                index = leftIndex ^ rightIndex
                result[index] += leftValue * rightValue
                if modulus is not None:
                    result[index] %= modulus

    return result


def xorPower(distribution, exponent, modulus=None):
    result = [0] * len(distribution)
    result[0] = 1
    base = [value % modulus for value in distribution] if modulus else distribution[:]

    while exponent:
        if exponent & 1:
            result = xorConvolve(result, base, modulus)
        exponent //= 2
        if exponent:
            base = xorConvolve(base, base, modulus)

    return result


def divisorGameWinningCount(n, k, modulus=None):
    distribution = grundyDistribution(n)
    finalDistribution = xorPower(distribution, k, modulus)

    if modulus is None:
        totalPositions = (n - 1) ** k
        return totalPositions - finalDistribution[0]

    totalPositions = pow(n - 1, k, modulus)
    return (totalPositions - finalDistribution[0]) % modulus


def runTests():
    assert divisorGameWinningCount(10, 5) == 40_085


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisorGameWinningCount(10 ** 7, 10 ** 12, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
