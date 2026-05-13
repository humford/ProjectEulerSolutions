import math
import time
from array import array
from fractions import Fraction


PROBLEM_LIMIT = 10_000_000


def bruteS(limit):
    total = Fraction(0)

    for m in range(2, limit + 1):
        for p in range(1, m + 1):
            for q in range(p + 1, m + 1):
                if p + q >= m and math.gcd(p, q) == 1:
                    total += Fraction(1, p * q)

    return total


def mobiusSieve(limit):
    mu = array("b", [0]) * (limit + 1)
    mu[1] = 1

    isComposite = bytearray(limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            mu[number] = -1

        for prime in primes:
            composite = number * prime
            if composite > limit:
                break

            isComposite[composite] = 1
            if number % prime == 0:
                mu[composite] = 0
                break

            mu[composite] = -mu[number]

    return mu


def quotientBlockData(limit):
    prefixIndices = {0}
    harmonicIndices = {0}

    start = 1
    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        prefixIndices.add(start - 1)
        prefixIndices.add(end)
        harmonicIndices.update(
            [quotient, quotient - 1, quotient // 2, (quotient - 1) // 2]
        )
        start = end + 1

    return prefixIndices, harmonicIndices


def buildSparsePrefixes(limit, mu):
    prefixIndices, harmonicIndices = quotientBlockData(limit)

    harmonics = {0: 0.0}
    squareHarmonics = {0: 0.0}
    mobiusOverN = {0: 0.0}
    mobiusOverNSquared = {0: 0.0}

    harmonicTotal = 0.0
    squareHarmonicTotal = 0.0
    mobiusOverNTotal = 0.0
    mobiusOverNSquaredTotal = 0.0

    for number in range(1, limit + 1):
        reciprocal = 1.0 / number
        reciprocalSquared = reciprocal * reciprocal

        harmonicTotal += reciprocal
        squareHarmonicTotal += reciprocalSquared

        if mu[number]:
            mobiusOverNTotal += mu[number] * reciprocal
            mobiusOverNSquaredTotal += mu[number] * reciprocalSquared

        if number in harmonicIndices:
            harmonics[number] = harmonicTotal
            squareHarmonics[number] = squareHarmonicTotal

        if number in prefixIndices:
            mobiusOverN[number] = mobiusOverNTotal
            mobiusOverNSquared[number] = mobiusOverNSquaredTotal

    return harmonics, squareHarmonics, mobiusOverN, mobiusOverNSquared


def blockCoefficients(limit, quotient, harmonics, squareHarmonics):
    half = quotient // 2
    lowerHalf = (quotient - 1) // 2

    totalPairReciprocal = (
        harmonics[quotient] * harmonics[quotient] - squareHarmonics[quotient]
    ) / 2.0

    firstRegionPairReciprocal = totalPairReciprocal - 0.5 * squareHarmonics[half]
    secondRegionPairReciprocal = 0.5 * squareHarmonics[half]

    firstRegionOneOverY = (
        2 * half
        - quotient
        + 1
        + quotient * harmonics[quotient - 1]
        - (quotient + 1) * harmonics[half]
    )

    allOneOverX = quotient * harmonics[quotient - 1] - (quotient - 1)
    firstRegionOneOverX = quotient * harmonics[lowerHalf] - 2 * lowerHalf
    secondRegionOneOverX = allOneOverX - firstRegionOneOverX

    linearCoefficient = firstRegionOneOverY - secondRegionOneOverX
    squareCoefficient = (
        firstRegionPairReciprocal + (limit + 1) * secondRegionPairReciprocal
    )

    return linearCoefficient, squareCoefficient


def summatoryS(limit):
    mu = mobiusSieve(limit)
    harmonics, squareHarmonics, mobiusOverN, mobiusOverNSquared = (
        buildSparsePrefixes(limit, mu)
    )

    total = 0.0
    start = 1

    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        linearCoefficient, squareCoefficient = blockCoefficients(
            limit, quotient, harmonics, squareHarmonics
        )

        total += linearCoefficient * (mobiusOverN[end] - mobiusOverN[start - 1])
        total += squareCoefficient * (
            mobiusOverNSquared[end] - mobiusOverNSquared[start - 1]
        )

        start = end + 1

    return total


def inverseCoprimeSum(limit=PROBLEM_LIMIT):
    return format(summatoryS(limit), ".4f")


def runTests():
    assert bruteS(2) == Fraction(1, 2)
    assert format(float(bruteS(10)), ".4f") == "6.9147"
    assert format(float(bruteS(100)), ".4f") == "58.2962"
    assert format(summatoryS(10), ".4f") == "6.9147"
    assert format(summatoryS(100), ".4f") == "58.2962"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = inverseCoprimeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
