from functools import lru_cache
import time


MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
INV6 = pow(6, MOD - 2, MOD)


def ceilLog2(n):
    if n <= 1:
        return 0
    return (n - 1).bit_length()


def repunit(n):
    value = 0
    for _ in range(n):
        value = 10 * value + 1
    return value


def sum1(n):
    if n <= 0:
        return 0
    return (n % MOD) * ((n + 1) % MOD) % MOD * INV2 % MOD


def sum2(n):
    if n <= 0:
        return 0
    return (n % MOD) * ((n + 1) % MOD) % MOD * ((2 * n + 1) % MOD) % MOD * INV6 % MOD


def rangeSum1(left, right):
    if left > right:
        return 0
    return (sum1(right) - sum1(left - 1)) % MOD


def rangeSum2(left, right):
    if left > right:
        return 0
    return (sum2(right) - sum2(left - 1)) % MOD


def tripleCountSum(left, right):
    if left > right:
        return 0
    count = (right - left + 1) % MOD
    s1 = rangeSum1(left, right)
    s2 = rangeSum2(left, right)
    return (s2 + 3 * s1 + 2 * count) * INV2 % MOD


def threshold(k):
    if k < 3:
        return 10**30
    return 3 * (1 << (k - 2)) + 2


def baseBadForBlock(powerOfTwo, offset):
    if offset < (powerOfTwo >> 1) + 2:
        return 0
    n = 2 * offset - powerOfTwo - 1
    return n * (n - 1) // 2


@lru_cache(maxsize=None)
def badCountForSum(total):
    if total <= 7:
        return 0

    k = (total - 1).bit_length() - 1
    powerOfTwo = 1 << k
    offset = total - powerOfTwo
    result = baseBadForBlock(powerOfTwo, offset)

    if k >= 3 and offset >= threshold(k):
        result += 3 * badCountForSum(offset)

    return result


def sumBaseBadBlockMod(powerOfTwo, maxOffset):
    if maxOffset <= 0:
        return 0

    start = (powerOfTwo >> 1) + 2
    if maxOffset < start:
        return 0

    left = start
    right = maxOffset
    count = (right - left + 1) % MOD
    sumL = rangeSum1(left, right)
    sumL2 = rangeSum2(left, right)
    const = ((powerOfTwo + 1) % MOD) * ((powerOfTwo + 2) % MOD) % MOD * INV2 % MOD

    return (2 * sumL2 - ((2 * powerOfTwo + 3) % MOD) * sumL + const * count) % MOD


def blockBadSumMod(powerOfTwo, maxOffset):
    if maxOffset <= 0:
        return 0

    k = powerOfTwo.bit_length() - 1
    result = sumBaseBadBlockMod(powerOfTwo, maxOffset)
    start = threshold(k)

    if start <= maxOffset:
        result += 3 * (badPrefixSumMod(maxOffset) - badPrefixSumMod(start - 1))

    return result % MOD


@lru_cache(maxsize=None)
def badPrefixSumMod(n):
    if n <= 0:
        return 0
    if n <= 16:
        return sum(badCountForSum(total) for total in range(1, n + 1)) % MOD

    powerOfTwo = 1 << (n.bit_length() - 1)
    if n == powerOfTwo:
        if powerOfTwo == 1:
            return 0
        half = powerOfTwo >> 1
        return (badPrefixSumMod(half) + blockBadSumMod(half, half)) % MOD

    return (badPrefixSumMod(powerOfTwo) + blockBadSumMod(powerOfTwo, n - powerOfTwo)) % MOD


def basePartMod(n):
    result = 0
    logValue = 1
    low = 2

    while low <= n:
        high = min(1 << logValue, n)
        result = (result + logValue * tripleCountSum(low, high)) % MOD
        logValue += 1
        low = (1 << (logValue - 1)) + 1

    return result


def H(n):
    return (basePartMod(n) + badPrefixSumMod(n)) % MOD


def singlePlateQuestions(n):
    return ceilLog2(n)


@lru_cache(maxsize=None)
def hBruteForce(a, b, c):
    a, b, c = sorted((a, b, c), reverse=True)
    total = a + b + c
    if total <= 1:
        return 0
    if b == 0 and c == 0:
        return singlePlateQuestions(a)

    best = 10**9
    plates = (a, b, c)
    for index, plate in enumerate(plates):
        if plate == 0:
            continue
        others = [plates[i] for i in range(3) if i != index]
        y, z = others

        for chosen in range(1, plate):
            best = min(
                best,
                1 + max(singlePlateQuestions(chosen), hBruteForce(plate - chosen, y, z)),
            )

        best = min(best, 1 + max(singlePlateQuestions(plate), hBruteForce(0, y, z)))

    return best


def HExactSmall(n):
    total = 0
    for s in range(1, n + 1):
        total += ((s + 2) * (s + 1) // 2) * ceilLog2(s)
        total += badCountForSum(s)
    return total


def runTests():
    assert hBruteForce(1, 2, 3) == 3
    assert hBruteForce(2, 3, 3) == 4
    assert HExactSmall(6) == 203
    assert HExactSmall(20) == 7_718
    assert HExactSmall(repunit(3)) == 1_634_144


def solve():
    return H(repunit(19))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
