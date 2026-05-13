import math
import time
from collections import deque


MOD = 1_234_567_891


def smallestPrimeFactorSieve(limit):
    spf = list(range(limit + 1))

    for n in range(2, math.isqrt(limit) + 1):
        if spf[n] == n:
            for multiple in range(n * n, limit + 1, n):
                if spf[multiple] == multiple:
                    spf[multiple] = n

    return spf


def factorList(n, spf):
    factors = []
    while n > 1:
        prime = spf[n]
        factors.append(prime)
        n //= prime
    return factors


def initialFactorState(n):
    spf = smallestPrimeFactorSieve(n)
    piles = []
    positions = []
    totalFactors = 0

    for value in range(2, n + 1):
        factors = factorList(value, spf)
        piles.append(factors)
        positions.append(0)
        totalFactors += len(factors)

    return piles, positions, totalFactors


def oneRound(piles, positions):
    extracted = [0] * len(piles)
    nextPiles = []
    nextPositions = []

    for index, factors in enumerate(piles):
        position = positions[index]
        extracted[index] = factors[position]
        position += 1
        if position < len(factors):
            nextPiles.append(factors)
            nextPositions.append(position)

    extracted.sort()
    nextPiles.append(extracted)
    nextPositions.append(0)

    return nextPiles, nextPositions, extracted


def directSum(n, rounds):
    piles, positions, _ = initialFactorState(n)

    for _ in range(rounds):
        piles, positions, _ = oneRound(piles, positions)

    total = 0
    for factors, position in zip(piles, positions):
        product = 1
        for value in factors[position:]:
            product *= value
        total += product
    return total


def simulateUntilPeriodic(n, extraColumns=10, stableRounds=2000, maxRounds=200000):
    piles, positions, totalFactors = initialFactorState(n)
    columnLimit = math.isqrt(2 * totalFactors) + extraColumns
    buffers = [None] + [deque(maxlen=k) for k in range(1, columnLimit + 1)]

    stableStreak = 0
    roundIndex = 0

    while roundIndex < maxRounds:
        roundIndex += 1
        piles, positions, extracted = oneRound(piles, positions)

        if roundIndex <= columnLimit:
            for column in range(1, columnLimit + 1):
                value = extracted[column - 1] if column <= len(extracted) else 1
                buffers[column].append(value)
            stableStreak = 0
            continue

        allRotating = True
        for column in range(1, columnLimit + 1):
            value = extracted[column - 1] if column <= len(extracted) else 1
            if buffers[column][0] != value:
                allRotating = False
            buffers[column].append(value)

        if allRotating:
            stableStreak += 1
            if stableStreak >= stableRounds:
                patterns = [[] for _ in range(columnLimit + 1)]
                maxColumn = 0
                for column in range(1, columnLimit + 1):
                    pattern = list(buffers[column])
                    patterns[column] = pattern
                    if any(value != 1 for value in pattern):
                        maxColumn = column
                return roundIndex, patterns, maxColumn
        else:
            stableStreak = 0

    raise RuntimeError("Periodicity was not detected")


def directSumMod(n, rounds, modulus=MOD):
    piles, positions, _ = initialFactorState(n)

    for _ in range(rounds):
        piles, positions, _ = oneRound(piles, positions)

    total = 0
    for factors, position in zip(piles, positions):
        product = 1
        for value in factors[position:]:
            product = product * value % modulus
        total = (total + product) % modulus
    return total


def S(n, rounds, modulus=MOD):
    if n <= 50 and rounds <= 5000:
        return directSum(n, rounds) % modulus

    endRound, patterns, maxColumn = simulateUntilPeriodic(n)

    if rounds <= endRound:
        return directSumMod(n, rounds, modulus)

    baseIndex = rounds - endRound - 1
    total = 0

    for age in range(maxColumn):
        sourceIndex = baseIndex - age
        if patterns[age + 1][sourceIndex % (age + 1)] == 1:
            continue

        product = 1
        for column in range(maxColumn, age, -1):
            value = patterns[column][sourceIndex % column]
            if value != 1:
                product = product * value % modulus
        total = (total + product) % modulus

    return total


def runTests():
    assert directSum(5, 3) == 21
    assert directSum(10, 100) == 257


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10_000, 10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
