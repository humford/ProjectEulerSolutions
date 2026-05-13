from math import comb, gcd
import time


MOD = 989_898_989


def modularInverse(n, modulus):
    oldR, r = modulus, n % modulus
    oldS, s = 0, 1

    while r:
        quotient = oldR // r
        oldR, r = r, oldR - quotient * r
        oldS, s = s, oldS - quotient * s

    if oldR != 1:
        raise ValueError("inverse does not exist")
    return oldS % modulus


def factorialTables(limit, modulus):
    factorials = [1] * (limit + 1)
    for i in range(1, limit + 1):
        factorials[i] = factorials[i - 1] * i % modulus

    inverseFactorials = [1] * (limit + 1)
    inverseFactorials[limit] = modularInverse(factorials[limit], modulus)
    for i in range(limit, 0, -1):
        inverseFactorials[i - 1] = inverseFactorials[i] * i % modulus

    return factorials, inverseFactorials


def fairArrangements(n, modulus=MOD):
    factorials, inverseFactorials = factorialTables(n, modulus)
    factorialN = factorials[n]
    total = 0

    for fourStepCount in range(n + 1):
        oneStepCount = n - fourStepCount
        if oneStepCount % 2:
            continue

        chooseStepTypes = (
            factorialN
            * inverseFactorials[fourStepCount]
            % modulus
            * inverseFactorials[oneStepCount]
            % modulus
        )
        highNet = min(fourStepCount, oneStepCount // 4)
        parity = fourStepCount % 2
        inner = 0

        for netFour in range(parity, highNet + 1, 2):
            plusFour = (fourStepCount + netFour) // 2
            plusOne = (oneStepCount - 4 * netFour) // 2
            waysFour = (
                factorials[fourStepCount]
                * inverseFactorials[plusFour]
                % modulus
                * inverseFactorials[fourStepCount - plusFour]
                % modulus
            )
            waysOne = (
                factorials[oneStepCount]
                * inverseFactorials[plusOne]
                % modulus
                * inverseFactorials[oneStepCount - plusOne]
                % modulus
            )
            term = waysFour * waysOne % modulus
            inner += term if netFour == 0 else 2 * term

        total = (total + chooseStepTypes * (inner % modulus)) % modulus

    return total


def fairArrangementsExact(n):
    total = 0
    for fourStepCount in range(n + 1):
        oneStepCount = n - fourStepCount
        if oneStepCount % 2:
            continue
        highNet = min(fourStepCount, oneStepCount // 4)
        parity = fourStepCount % 2
        inner = 0
        for netFour in range(parity, highNet + 1, 2):
            plusFour = (fourStepCount + netFour) // 2
            plusOne = (oneStepCount - 4 * netFour) // 2
            term = comb(fourStepCount, plusFour) * comb(oneStepCount, plusOne)
            inner += term if netFour == 0 else 2 * term
        total += comb(n, fourStepCount) * inner
    return total


def runTests():
    assert fairArrangementsExact(2) == 4
    assert fairArrangementsExact(10) == 63_594
    assert fairArrangements(2) == 4
    assert fairArrangements(10) == 63_594


def solve():
    return fairArrangements(9898)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
