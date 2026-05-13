import time


MODULUS = 1_000_000_007


def grundyValuesForTwoSplits(stones):
    values = [0] * (stones + 1)
    for pileSize in range(2, stones + 1):
        values[pileSize] = 1 if pileSize % 2 == 0 else 0
    return values


def grundyValuesForThreeSplits(stones):
    values = [0] * (stones + 1)
    for pileSize in range(2, stones + 1):
        seen = set()

        for first in range(1, pileSize // 2 + 1):
            second = pileSize - first
            seen.add(values[first] ^ values[second])

        for first in range(1, pileSize // 3 + 1):
            for second in range(first, (pileSize - first) // 2 + 1):
                third = pileSize - first - second
                seen.add(values[first] ^ values[second] ^ values[third])

        mex = 0
        while mex in seen:
            mex += 1
        values[pileSize] = mex

    return values


def grundyValuesForAtLeastFourSplits(stones):
    return [0] + [pileSize - 1 for pileSize in range(1, stones + 1)]


def enumeratedGrundyValues(stones, maxSplit):
    values = [0] * (stones + 1)
    for pileSize in range(2, stones + 1):
        seen = set()

        for first in range(1, pileSize // 2 + 1):
            second = pileSize - first
            seen.add(values[first] ^ values[second])

        if maxSplit >= 3:
            for first in range(1, pileSize // 3 + 1):
                for second in range(first, (pileSize - first) // 2 + 1):
                    third = pileSize - first - second
                    seen.add(values[first] ^ values[second] ^ values[third])

        if maxSplit >= 4:
            for first in range(1, pileSize // 4 + 1):
                for second in range(first, (pileSize - first) // 3 + 1):
                    for third in range(second, (pileSize - first - second) // 2 + 1):
                        fourth = pileSize - first - second - third
                        seen.add(
                            values[first] ^
                            values[second] ^
                            values[third] ^
                            values[fourth]
                        )

        mex = 0
        while mex in seen:
            mex += 1
        values[pileSize] = mex

    return values


def grundyValues(stones, maxSplit):
    if maxSplit == 2:
        return grundyValuesForTwoSplits(stones)
    if maxSplit == 3:
        return grundyValuesForThreeSplits(stones)
    return grundyValuesForAtLeastFourSplits(stones)


def winningPartitionCount(stones, values):
    xorLimit = 1
    while xorLimit <= max(values):
        xorLimit *= 2
    xorLimit *= 2

    counts = [[0] * xorLimit for _ in range(stones + 1)]
    counts[0][0] = 1
    for pileSize in range(1, stones + 1):
        grundy = values[pileSize]
        for total in range(pileSize, stones + 1):
            previous = counts[total - pileSize]
            current = counts[total]
            for xorValue, count in enumerate(previous):
                if count:
                    current[xorValue ^ grundy] = (
                        current[xorValue ^ grundy] + count
                    ) % MODULUS

    return (sum(counts[stones]) - counts[stones][0]) % MODULUS


def winningPositionCount(stones, maxSplit):
    return winningPartitionCount(stones, grundyValues(stones, maxSplit))


def scatterstoneTotal(stones):
    if stones < 2:
        return 0

    twoSplitCount = winningPositionCount(stones, 2)
    threeSplitCount = winningPositionCount(stones, 3)
    atLeastFourCount = winningPositionCount(stones, 4)
    return (twoSplitCount + threeSplitCount + (stones - 3) * atLeastFourCount) % MODULUS


def runTests():
    assert winningPositionCount(5, 2) == 3
    assert winningPositionCount(5, 3) == 5
    assert enumeratedGrundyValues(30, 4) == grundyValuesForAtLeastFourSplits(30)
    assert scatterstoneTotal(7) == 66
    assert scatterstoneTotal(10) == 291


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = scatterstoneTotal(200)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
