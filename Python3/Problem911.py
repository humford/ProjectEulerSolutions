from math import exp, log
from multiprocessing import cpu_count, get_context
import time


TARGET_N_MIN = 0
TARGET_N_MAX = 50
TARGET_START_LEVEL = 16
TARGET_END_LEVEL = 19


def rhoTruncation(n, level):
    denominator = 1 << (1 << level)
    numerator = 0

    for index in range(level + 1):
        numerator += 1 << ((1 << level) + n - (1 << index))

    return numerator, denominator


def commonPrefixLogMean(n, level):
    numeratorA, denominatorA = rhoTruncation(n, level)
    numeratorB, denominatorB = rhoTruncation(n, level + 1)

    integerPart = numeratorA // denominatorA
    numeratorA -= integerPart * denominatorA
    integerPart = numeratorB // denominatorB
    numeratorB -= integerPart * denominatorB

    numeratorA, denominatorA = denominatorA, numeratorA
    numeratorB, denominatorB = denominatorB, numeratorB

    total = 0.0
    count = 0

    while denominatorA and denominatorB:
        quotientA = numeratorA // denominatorA
        quotientB = numeratorB // denominatorB
        if quotientA != quotientB:
            break

        total += log(quotientA)
        count += 1
        numeratorA, denominatorA = denominatorA, numeratorA - quotientA * denominatorA
        numeratorB, denominatorB = denominatorB, numeratorB - quotientB * denominatorB

    if count == 0:
        raise ValueError("no common continued-fraction prefix")

    return total / count


def averageLogMeanForLevel(level, nMin=TARGET_N_MIN, nMax=TARGET_N_MAX, processes=None):
    values = list(range(nMin, nMax + 1))

    if processes is None:
        processes = min(8, cpu_count() or 1)
    processes = max(1, min(processes, len(values)))

    if processes == 1:
        means = [commonPrefixLogMean(n, level) for n in values]
    else:
        try:
            context = get_context("fork")
        except ValueError:
            means = [commonPrefixLogMean(n, level) for n in values]
        else:
            with context.Pool(processes) as pool:
                means = pool.starmap(
                    commonPrefixLogMean,
                    [(n, level) for n in values],
                )

    return sum(means) / len(means)


def aitkenAcceleratedLimit(logMeans):
    levels = sorted(logMeans)
    richardson = []

    for level in levels[1:]:
        richardson.append(2 * logMeans[level] - logMeans[level - 1])

    if len(richardson) < 3:
        raise ValueError("need at least four levels for acceleration")

    previous, current, nextValue = richardson[-3:]
    denominator = nextValue - 2 * current + previous
    return nextValue - (nextValue - current) ** 2 / denominator


def estimateSingleKhinchin(n, startLevel, endLevel):
    logMeans = {
        level: commonPrefixLogMean(n, level)
        for level in range(startLevel, endLevel + 1)
    }
    return exp(aitkenAcceleratedLimit(logMeans))


def solve():
    logMeans = {
        level: averageLogMeanForLevel(level)
        for level in range(TARGET_START_LEVEL, TARGET_END_LEVEL + 1)
    }
    return f"{exp(aitkenAcceleratedLimit(logMeans)):.6f}"


def runTests():
    assert f"{estimateSingleKhinchin(2, 10, 13):.6f}" == "2.059767"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == "5679.934966"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
