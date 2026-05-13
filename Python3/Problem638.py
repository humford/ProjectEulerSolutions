import math
import time


MODULUS = 1_000_000_007


def combinationMod(n, r, modulus):
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    numerator = 1
    denominator = 1
    for index in range(1, r + 1):
        numerator = numerator * (n - r + index) % modulus
        denominator = denominator * index % modulus
    return numerator * pow(denominator, modulus - 2, modulus) % modulus


def weightedPathSum(width, height, weight, modulus=None):
    if weight == 1 and modulus is None:
        return math.comb(width + height, width)
    if modulus is None:
        values = [[0] * (height + 1) for _ in range(width + 1)]
        values[0][0] = 1
        for x in range(width + 1):
            for y in range(height + 1):
                if x == 0 and y == 0:
                    continue
                total = 0
                if y > 0:
                    total += values[x][y - 1]
                if x > 0:
                    total += values[x - 1][y] * weight ** y
                values[x][y] = total
        return values[width][height]

    if weight == 1:
        return combinationMod(width + height, width, modulus)

    numerator = 1
    denominator = 1
    denominatorPower = 1
    numeratorPower = pow(weight, height, modulus)
    numeratorZeros = 0
    denominatorZeros = 0

    for index in range(1, width + 1):
        denominatorPower = denominatorPower * weight % modulus
        numeratorPower = numeratorPower * weight % modulus

        numeratorFactor = (numeratorPower - 1) % modulus
        denominatorFactor = (denominatorPower - 1) % modulus
        if numeratorFactor == 0:
            numeratorZeros += 1
        else:
            numerator = numerator * numeratorFactor % modulus
        if denominatorFactor == 0:
            denominatorZeros += 1
        else:
            denominator = denominator * denominatorFactor % modulus

    if numeratorZeros != denominatorZeros:
        if numeratorZeros > denominatorZeros:
            return 0
        raise ValueError("uncancelled zero denominator in q-binomial product")

    return numerator * pow(denominator, modulus - 2, modulus) % modulus


def weightedPathTargetTotal():
    total = 0
    for exponent in range(1, 8):
        side = 10 ** exponent + exponent
        total = (total + weightedPathSum(side, side, exponent, MODULUS)) % MODULUS
    return total


def runTests():
    assert weightedPathSum(2, 2, 1) == 6
    assert weightedPathSum(2, 2, 2) == 35
    assert weightedPathSum(10, 10, 1) == 184_756
    assert weightedPathSum(15, 10, 3, MODULUS) == 880_419_838
    assert weightedPathSum(10_000, 10_000, 4, MODULUS) == 395_913_804


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = weightedPathTargetTotal()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
