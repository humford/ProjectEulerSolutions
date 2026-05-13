from bisect import bisect_left
from math import gcd
import time


MODULUS = 1_000_000_007
TAU_MULTIPLIER = 1_000_000_007
TARGET_M = 100


def extendedGcd(a, b):
    oldR, r = a, b
    oldS, s = 1, 0
    oldT, t = 0, 1

    while r:
        quotient = oldR // r
        oldR, r = r, oldR - quotient * r
        oldS, s = s, oldS - quotient * s
        oldT, t = t, oldT - quotient * t

    return oldR, oldS, oldT


def inverseMod(value, modulus):
    if modulus == 1:
        return 0
    divisor, inverse, _ = extendedGcd(value % modulus, modulus)
    if divisor != 1:
        raise ValueError("inverse does not exist")
    return inverse % modulus


def rankSmall(permutation):
    n = len(permutation)
    factorials = [1] * (n + 1)
    for index in range(2, n + 1):
        factorials[index] = index * factorials[index - 1]

    used = [False] * (n + 1)
    rank = 1
    for index, value in enumerate(permutation):
        smallerUnused = sum(1 for x in range(1, value) if not used[x])
        rank += smallerUnused * factorials[n - index - 1]
        used[value] = True

    return rank


def lcmUpTo(limit):
    value = 1

    for number in range(2, limit + 1):
        value = value // gcd(value, number) * number

    return value


def buildCycles(m, n):
    cycles = [[] for _ in range(m + 1)]
    cycleLength = [0] * (n + 1)
    cycleOffset = [0] * (n + 1)

    if n == 1:
        cycles[1] = [1]
        cycleLength[1] = 1
        return cycles, cycleLength, cycleOffset

    inverseMultiplier = inverseMod(TAU_MULTIPLIER % n, n)

    def tauInverse(x):
        value = inverseMultiplier * ((x - 1) % n) % n
        return n if value == 0 else value

    for length in range(1, m + 1):
        start = length * (length - 1) // 2 + 1
        cycle = [tauInverse(x) for x in range(start, start + length)]
        cycles[length] = cycle

        for offset, element in enumerate(cycle):
            cycleLength[element] = length
            cycleOffset[element] = offset

    return cycles, cycleLength, cycleOffset


def factorialsMod(limit, modulus):
    factorials = [1] * (limit + 1)

    for index in range(2, limit + 1):
        factorials[index] = factorials[index - 1] * index % modulus

    return factorials


def comparisonTables(cycles, m, periodMod):
    gcdTable = [[0] * (m + 1) for _ in range(m + 1)]
    scale = [[0] * (m + 1) for _ in range(m + 1)]
    comparisons = [[[] for _ in range(m + 1)] for __ in range(m + 1)]

    for a in range(1, m + 1):
        for b in range(1, m + 1):
            divisor = gcd(a, b)
            period = a // divisor * b
            gcdTable[a][b] = divisor
            scale[a][b] = periodMod * pow(period % MODULUS, MODULUS - 2, MODULUS) % MODULUS

            aValues = cycles[a]
            bValues = cycles[b]
            aByResidue = [aValues[residue::divisor] for residue in range(divisor)]
            bByResidue = [
                sorted(bValues[residue::divisor])
                for residue in range(divisor)
            ]

            counts = [0] * divisor
            for difference in range(divisor):
                total = 0
                for residue in range(divisor):
                    other = (residue - difference) % divisor
                    sortedB = bByResidue[other]
                    for value in aByResidue[residue]:
                        total += bisect_left(sortedB, value)
                counts[difference] = total

            comparisons[a][b] = counts

    return comparisons, gcdTable, scale


def sumRanksOverPeriod(m):
    n = m * (m + 1) // 2
    factorials = factorialsMod(n, MODULUS)
    weights = [0] * (n + 1)
    for position in range(1, n + 1):
        weights[position] = factorials[n - position]

    cycles, cycleLength, cycleOffset = buildCycles(m, n)
    period = lcmUpTo(m)
    periodMod = period % MODULUS
    comparisons, gcdTable, scale = comparisonTables(cycles, m, periodMod)

    total = 0
    threshold = 1 << 62

    for i in range(1, n):
        weight = weights[i]
        lengthI = cycleLength[i]
        offsetI = cycleOffset[i]
        for j in range(i + 1, n + 1):
            lengthJ = cycleLength[j]
            divisor = gcdTable[lengthI][lengthJ]
            difference = 0 if divisor == 1 else (offsetI - cycleOffset[j]) % divisor
            smallCount = comparisons[lengthI][lengthJ][difference]
            if smallCount:
                total += weight * (scale[lengthI][lengthJ] * smallCount % MODULUS)
                if total >= threshold:
                    total %= MODULUS

    return (periodMod + total) % MODULUS, periodMod


def P(m):
    periodSum, periodMod = sumRanksOverPeriod(m)
    factorial = 1
    for index in range(2, m + 1):
        factorial = factorial * index % MODULUS

    return periodSum * factorial % MODULUS * pow(periodMod, MODULUS - 2, MODULUS) % MODULUS


def solve():
    return P(TARGET_M)


def runTests():
    assert rankSmall([2, 1, 3]) == 3
    assert P(2) == 4
    assert P(3) == 780
    assert P(4) == 38810300
    assert solve() == 343557869


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
