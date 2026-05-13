from math import isqrt
import time


def integerRoot(n, exponent):
    if exponent == 2:
        return isqrt(n)

    root = int(n ** (1.0 / exponent))
    while (root + 1) ** exponent <= n:
        root += 1
    while root**exponent > n:
        root -= 1
    return root


def progressionParameters(base, exponent):
    largestTerm = base**exponent
    progressionSum = base ** (exponent + 1) - (base - 1) ** (exponent + 1)
    return largestTerm, progressionSum


def maxSearchExponent(limit):
    exponent = 2
    while 2**exponent <= limit:
        exponent += 1
    return exponent


def nextEventForExponent(currentBest, limit, exponent, cutoff):
    maxBase = integerRoot(limit, exponent)
    if maxBase < 2:
        return None

    bestEvent = cutoff
    bestBase = None
    candidates = {2, maxBase}
    center = integerRoot(max(1, currentBest // (exponent + 1)), exponent)
    for offset in range(-8, 9):
        base = center + offset
        if 2 <= base <= maxBase:
            candidates.add(base)

    def evaluate(base):
        nonlocal bestEvent, bestBase
        largestTerm, progressionSum = progressionParameters(base, exponent)
        event = largestTerm * (currentBest // progressionSum + 1)
        if event < bestEvent:
            bestEvent = event
            bestBase = base

    for base in candidates:
        evaluate(base)

    stack = [(2, maxBase)]
    while stack:
        lowerBase, upperBase = stack.pop()
        if lowerBase > upperBase:
            continue

        upperLargest, upperSum = progressionParameters(upperBase, exponent)
        lowerBound = max(
            lowerBase**exponent,
            currentBest * upperLargest // upperSum + 1,
        )
        if lowerBound >= bestEvent:
            continue

        if upperBase - lowerBase <= 64:
            for base in range(lowerBase, upperBase + 1):
                evaluate(base)
        else:
            middle = (lowerBase + upperBase) // 2
            evaluate(middle)
            stack.append((lowerBase, middle - 1))
            stack.append((middle + 1, upperBase))

    if bestBase is None:
        return None
    return bestEvent, bestBase


def bestProgressionAt(limit):
    best = 0
    bestPattern = None

    for exponent in range(maxSearchExponent(limit), 1, -1):
        maxBase = integerRoot(limit, exponent)
        if maxBase < 2:
            continue

        candidates = {2, maxBase}
        for multiple in range(1, 16):
            center = integerRoot(limit // multiple, exponent)
            for offset in range(-4, 5):
                base = center + offset
                if 2 <= base <= maxBase:
                    candidates.add(base)

        def evaluate(base):
            nonlocal best, bestPattern
            largestTerm, progressionSum = progressionParameters(base, exponent)
            multiplier = limit // largestTerm
            value = progressionSum * multiplier
            if value > best:
                best = value
                bestPattern = (base, exponent + 1, multiplier)

        for base in candidates:
            evaluate(base)

        stack = [(2, maxBase)]
        while stack:
            lowerBase, upperBase = stack.pop()
            if lowerBase > upperBase:
                continue

            _, upperSum = progressionParameters(upperBase, exponent)
            upperBound = (limit // (lowerBase**exponent)) * upperSum
            if upperBound <= best:
                continue

            if upperBase - lowerBase <= 64:
                for base in range(lowerBase, upperBase + 1):
                    evaluate(base)
            else:
                middle = (lowerBase + upperBase) // 2
                evaluate(middle)
                stack.append((lowerBase, middle - 1))
                stack.append((middle + 1, upperBase))

    return best, bestPattern


def recordProgressions(limit):
    records = []
    currentBest = 0
    maxExponent = maxSearchExponent(limit)

    while True:
        nextEvent = limit + 1
        for exponent in range(maxExponent, 1, -1):
            event = nextEventForExponent(currentBest, limit, exponent, nextEvent)
            if event is not None and event[0] < nextEvent:
                nextEvent = event[0]

        if nextEvent > limit:
            break

        value, pattern = bestProgressionAt(nextEvent)
        if value <= currentBest:
            raise RuntimeError("record search failed to advance")
        records.append((nextEvent, value, pattern))
        currentBest = value

    return records


def alternatingSignSum(start, stop):
    if stop < start or (stop - start + 1) % 2 == 0:
        return 0
    return 1 if start % 2 == 0 else -1


def maxProgressionSum(k):
    return bestProgressionAt(k)[0]


def alternatingProgressionSum(n):
    records = recordProgressions(n)
    total = 0

    for index, (start, value, _) in enumerate(records):
        stop = records[index + 1][0] - 1 if index + 1 < len(records) else n
        total += value * alternatingSignSum(max(4, start), stop)

    return total


def runTests():
    assert maxProgressionSum(4) == 7
    assert maxProgressionSum(10) == 19
    assert maxProgressionSum(12) == 21
    assert maxProgressionSum(1_000) == 3_439
    assert alternatingProgressionSum(1_000) == 2_268


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = alternatingProgressionSum(10 ** 17)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
