import time

import numpy as np


MODULUS = 11**8
EXPONENT_PERIOD = 10 * 11**7
PROBLEM_LIMIT = 10_000_000


def totientAndMobius(limit):
    totients = np.arange(limit + 1, dtype=np.int64)
    mobius = np.ones(limit + 1, dtype=np.int8)
    totients[0] = 0
    mobius[0] = 0

    for prime in range(2, limit + 1):
        if totients[prime] == prime:
            totients[prime::prime] -= totients[prime::prime] // prime
            mobius[prime::prime] *= -1
            square = prime * prime
            if square <= limit:
                mobius[square::square] = 0

    return totients, mobius


def coprimeRectanglePrefix(limit, mobius):
    divisors = np.arange(1, limit + 1, dtype=np.int64)
    weights = (
        mobius[1:].astype(np.int64) * (limit // divisors + 1)
    ) % EXPONENT_PERIOD
    increments = np.zeros(limit + 1, dtype=np.int64)

    for divisor, weight in enumerate(weights, start=1):
        if weight:
            increments[divisor::divisor] += weight
            increments[divisor::divisor] %= EXPONENT_PERIOD

    return np.cumsum(increments, dtype=np.int64) % EXPONENT_PERIOD


def directionMultiplicityMod(width, limit, coprimePrefix, totientPrefix):
    quotient = limit // width
    return (
        int(coprimePrefix[quotient])
        - width * int(totientPrefix[quotient])
    ) % EXPONENT_PERIOD


def halfNonDiagonalExponent(limit, totients, coprimePrefix, totientPrefix):
    exponent = 0
    for width in range(1, limit + 1):
        multiplicity = directionMultiplicityMod(
            width, limit, coprimePrefix, totientPrefix
        )
        exponent += 3 * int(totients[width]) * multiplicity
        exponent %= EXPONENT_PERIOD
    return exponent


def badSubsetCount(limit, totients, coprimePrefix, totientPrefix,
                   halfExponent):
    semicirclePower = pow(2, halfExponent, MODULUS)
    total = 0

    for width in range(1, limit + 1):
        multiplicity = directionMultiplicityMod(
            width, limit, coprimePrefix, totientPrefix
        )
        total += int(totients[width]) * (
            semicirclePower
            - pow(2, (halfExponent - multiplicity) % EXPONENT_PERIOD, MODULUS)
        )
        total %= MODULUS

    return (1 + 6 * total) % MODULUS


def equalMixtureSubsetCount(limit):
    totients, mobius = totientAndMobius(limit)
    coprimePrefix = coprimeRectanglePrefix(limit, mobius)
    totientPrefix = np.cumsum(totients, dtype=np.int64) % EXPONENT_PERIOD

    halfExponent = halfNonDiagonalExponent(
        limit, totients, coprimePrefix, totientPrefix
    )
    allSubsets = pow(2, (2 * halfExponent + 1) % EXPONENT_PERIOD, MODULUS)
    badSubsets = badSubsetCount(
        limit, totients, coprimePrefix, totientPrefix, halfExponent
    )
    return (allSubsets - badSubsets) % MODULUS


def runTests():
    assert equalMixtureSubsetCount(1) == 103
    assert equalMixtureSubsetCount(2) == 520_447
    assert equalMixtureSubsetCount(10) == 82_608_406
    assert equalMixtureSubsetCount(500) == 13_801_403


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = equalMixtureSubsetCount(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
