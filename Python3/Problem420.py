import time
from collections import defaultdict
from math import gcd, isqrt


def squareMatrix(a, b, c, d):
    return (
        a * a + b * c,
        b * (a + d),
        c * (a + d),
        d * d + b * c,
    )


def bruteF(limit):
    rootsBySquare = defaultdict(int)

    for a in range(1, int(limit**0.5) + 1):
        for d in range(1, int(limit**0.5) + 1):
            remaining = limit - 1 - a * a - d * d

            if remaining < 2:
                continue

            for b in range(1, remaining // 2 + 1):
                for c in range(1, remaining // (2 * b) + 1):
                    rootsBySquare[squareMatrix(a, b, c, d)] += 1

    return sum(1 for rootCount in rootsBySquare.values() if rootCount >= 2)


def divisorCounts(limit):
    counts = [0] * (limit + 1)

    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            counts[multiple] += 1

    return counts


def matrixCount(limit):
    maxTrace = isqrt(2 * limit - 1)
    divisorCount = divisorCounts(maxTrace * maxTrace // 4 + 1)
    total = 0

    for firstTrace in range(1, maxTrace + 1):
        firstTraceSquared = firstTrace * firstTrace

        for secondTrace in range(firstTrace + 1, maxTrace + 1):
            secondTraceSquared = secondTrace * secondTrace
            squareTraceNumerator = firstTraceSquared + secondTraceSquared

            if squareTraceNumerator >= 2 * limit:
                break
            if squareTraceNumerator % 2:
                continue

            traceLcm = firstTrace * secondTrace // gcd(firstTrace, secondTrace)
            maxDiagonalDifference = firstTraceSquared - 1
            minMultiplier = (
                -maxDiagonalDifference + traceLcm - 1
            ) // traceLcm
            maxMultiplier = maxDiagonalDifference // traceLcm
            rootProduct = firstTraceSquared * secondTraceSquared
            lcmSquared = traceLcm * traceLcm

            for multiplier in range(minMultiplier, maxMultiplier + 1):
                diagonalDifference = multiplier * traceLcm
                firstDifference = diagonalDifference // firstTrace
                secondDifference = diagonalDifference // secondTrace

                if (firstDifference - firstTrace) % 2:
                    continue
                if (secondDifference - secondTrace) % 2:
                    continue

                offDiagonalProductNumerator = (
                    rootProduct - diagonalDifference * diagonalDifference
                )

                if offDiagonalProductNumerator % 4:
                    continue

                offDiagonalProduct = offDiagonalProductNumerator // 4

                if offDiagonalProduct % lcmSquared:
                    continue

                total += divisorCount[offDiagonalProduct // lcmSquared]

    return total


def runTests():
    assert squareMatrix(2, 3, 12, 2) == (40, 12, 48, 40)
    assert squareMatrix(6, 1, 4, 6) == (40, 12, 48, 40)
    assert bruteF(50) == 7
    assert matrixCount(50) == 7
    assert matrixCount(1000) == 1019


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = matrixCount(10**7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
