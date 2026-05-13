from functools import lru_cache
import time


MOD = 1_000_000_007
TARGET_N = 10
MAX_ROW = 2 * TARGET_N - 1


INDEPENDENT_ROW_MASKS = [[] for _ in range(MAX_ROW + 1)]
for length in range(MAX_ROW + 1):
    masks = []
    for mask in range(1 << length):
        if mask & (mask << 1) == 0:
            masks.append(mask)
    INDEPENDENT_ROW_MASKS[length] = masks


def subsetSums(values, bits):
    sums = values[:]

    for bit in range(bits):
        step = 1 << bit
        block = step << 1
        for start in range(0, 1 << bits, block):
            for mask in range(start + step, start + block):
                sums[mask] = (sums[mask] + sums[mask - step]) % MOD

    return sums


@lru_cache(maxsize=None)
def countIndependentSets(rowLengths):
    if not rowLengths:
        return 1

    firstLength = rowLengths[0]
    dp = [0] * (1 << firstLength)
    for mask in INDEPENDENT_ROW_MASKS[firstLength]:
        dp[mask] = 1

    for previousLength, nextLength in zip(rowLengths, rowLengths[1:]):
        if abs(nextLength - previousLength) != 1:
            raise ValueError("adjacent rows must differ by one")

        compatiblePrefixSums = subsetSums(dp, previousLength)
        nextDp = [0] * (1 << nextLength)
        fullPreviousMask = (1 << previousLength) - 1

        for nextMask in INDEPENDENT_ROW_MASKS[nextLength]:
            if nextLength == previousLength + 1:
                blocked = nextMask | (nextMask >> 1)
            else:
                blocked = nextMask | (nextMask << 1)

            allowed = fullPreviousMask ^ (blocked & fullPreviousMask)
            nextDp[nextMask] = compatiblePrefixSums[allowed]

        dp = nextDp

    return sum(dp[mask] for mask in INDEPENDENT_ROW_MASKS[rowLengths[-1]]) % MOD


@lru_cache(maxsize=None)
def hexagonTilings(sideLength):
    increasing = tuple(range(sideLength, 2 * sideLength))
    decreasing = tuple(range(2 * sideLength - 2, sideLength - 1, -1))
    return countIndependentSets(increasing + decreasing)


@lru_cache(maxsize=None)
def cornerTilings(baseLength, height):
    rowCount = height - 1
    rows = tuple(max(0, baseLength - 2 - row) for row in range(rowCount))
    return countIndependentSets(rows)


@lru_cache(maxsize=None)
def reducedDodecagonTilings(longSide, shortSide):
    if shortSide == 0:
        return hexagonTilings(longSide)

    total = 1 if (longSide == 1 and shortSide == 1) else 0

    for nextShortSide in range(longSide):
        corner = cornerTilings(longSide, longSide - nextShortSide)
        total += (
            reducedDodecagonTilings(shortSide, nextShortSide)
            * pow(corner, 6, MOD)
        )

    return total % MOD


def T(sideLength):
    singleUnitDodecagonCorrection = 1 if sideLength == 1 else 0
    return (2 * reducedDodecagonTilings(sideLength, sideLength) - singleUnitDodecagonCorrection) % MOD


def runTests():
    assert hexagonTilings(1) == 2
    assert T(1) == 5
    assert T(2) == 48


def solve():
    return T(TARGET_N)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
