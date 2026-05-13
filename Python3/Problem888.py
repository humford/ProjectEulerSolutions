from math import comb
import time


TARGET_N = 12_491_249
TARGET_M = 1249
MODULUS = 912_491_249
PERIOD_START = 322
PERIOD = 11_060
REMOVE_OPTIONS = (1, 2, 4, 9)
CHARACTER_COUNT = 16


def isPrime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2

    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2

    return True


def computeGrundy(limit):
    values = [0] * (limit + 1)

    for stones in range(1, limit + 1):
        seen = 0

        for remove in REMOVE_OPTIONS:
            if stones >= remove:
                seen |= 1 << values[stones - remove]

        for left in range(1, stones // 2 + 1):
            seen |= 1 << (values[left] ^ values[stones - left])

        mex = 0
        while seen & (1 << mex):
            mex += 1
        values[stones] = mex

    return values


def validatedGrundyPrefix():
    validationLimit = 2 * PERIOD_START + 2 * PERIOD
    values = computeGrundy(validationLimit)

    assert max(values) < CHARACTER_COUNT
    for stones in range(PERIOD_START, validationLimit - PERIOD + 1):
        assert values[stones] == values[stones + PERIOD]

    return values


def grundyCountsUpTo(limit, values):
    counts = [0] * CHARACTER_COUNT

    if limit < PERIOD_START:
        for stones in range(1, limit + 1):
            counts[values[stones]] += 1
        return counts

    for stones in range(1, PERIOD_START):
        counts[values[stones]] += 1

    periodCounts = [0] * CHARACTER_COUNT
    for stones in range(PERIOD_START, PERIOD_START + PERIOD):
        periodCounts[values[stones]] += 1

    periodicTerms = limit - PERIOD_START + 1
    fullPeriods, remainder = divmod(periodicTerms, PERIOD)

    for grundyValue in range(CHARACTER_COUNT):
        counts[grundyValue] += fullPeriods * periodCounts[grundyValue]

    for stones in range(PERIOD_START, PERIOD_START + remainder):
        counts[values[stones]] += 1

    return counts


def exactCoefficient(totalTypes, pileCount, positiveTypes):
    negativeTypes = totalTypes - positiveTypes

    def multisetCoefficient(typeCount, selected):
        if selected == 0:
            return 1
        if typeCount == 0:
            return 0
        return comb(typeCount + selected - 1, selected)

    total = 0
    for selectedPositive in range(pileCount + 1):
        selectedNegative = pileCount - selectedPositive
        total += (
            multisetCoefficient(positiveTypes, selectedPositive)
            * ((-1) ** selectedNegative)
            * multisetCoefficient(negativeTypes, selectedNegative)
        )

    return total


def modularCoefficient(totalTypes, pileCount, positiveTypes, modulus):
    negativeTypes = totalTypes - positiveTypes
    inverses = [0] + [pow(index, modulus - 2, modulus) for index in range(1, pileCount + 1)]

    def negativeBinomialSeries(typeCount):
        series = [0] * (pileCount + 1)
        series[0] = 1

        if typeCount == 0:
            return series

        value = 1
        for selected in range(1, pileCount + 1):
            value *= (typeCount + selected - 1) % modulus
            value %= modulus
            value *= inverses[selected]
            value %= modulus
            series[selected] = value

        return series

    positiveSeries = negativeBinomialSeries(positiveTypes)
    negativeSeries = negativeBinomialSeries(negativeTypes)

    total = 0
    for selectedPositive in range(pileCount + 1):
        selectedNegative = pileCount - selectedPositive
        term = positiveSeries[selectedPositive] * negativeSeries[selectedNegative]
        if selectedNegative % 2:
            total -= term
        else:
            total += term

    return total % modulus


def characterPositiveCount(counts, character):
    return sum(
        count
        for grundyValue, count in enumerate(counts)
        if ((grundyValue & character).bit_count() % 2) == 0
    )


def SExact(limit, pileCount):
    values = computeGrundy(limit)
    counts = grundyCountsUpTo(limit, values)
    total = 0

    for character in range(CHARACTER_COUNT):
        positiveTypes = characterPositiveCount(counts, character)
        total += exactCoefficient(limit, pileCount, positiveTypes)

    assert total % CHARACTER_COUNT == 0
    return total // CHARACTER_COUNT


def SMod(limit, pileCount, modulus):
    assert isPrime(modulus)

    values = validatedGrundyPrefix()
    counts = grundyCountsUpTo(limit, values)
    total = 0

    for character in range(CHARACTER_COUNT):
        positiveTypes = characterPositiveCount(counts, character)
        total += modularCoefficient(limit, pileCount, positiveTypes, modulus)
        total %= modulus

    return total * pow(CHARACTER_COUNT, modulus - 2, modulus) % modulus


def solve():
    return SMod(TARGET_N, TARGET_M, MODULUS)


def runTests():
    assert SExact(12, 4) == 204
    assert SExact(124, 9) == 2259208528408


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 227429102
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
