import time


MODULUS = 1_000_000_007
INVERSE_3 = pow(3, MODULUS - 2, MODULUS)
INVERSE_7 = pow(7, MODULUS - 2, MODULUS)


def sumPowersOfEight(count):
    if count <= 0:
        return 0
    return (pow(8, count, MODULUS) - 1) * INVERSE_7 % MODULUS


def sumPowersOfFour(m):
    if m <= 0:
        return 0
    return (pow(4, m + 1, MODULUS) - 4) * INVERSE_3 % MODULUS


def offsetPrefixSum(limit):
    if limit <= 0:
        return 0

    termSum = 0
    prefixSum = 0
    power2 = 1
    power4 = 1

    for _ in range(limit):
        termSum = (2 * termSum + (power2 + 2) * power4) % MODULUS
        prefixSum = (prefixSum + termSum) % MODULUS
        power2 = (2 * power2) % MODULUS
        power4 = (4 * power4) % MODULUS

    return prefixSum


def winningBlackboardSum(exponent):
    if exponent < 0:
        raise ValueError("exponent must be non-negative")

    if exponent % 2 == 0:
        half = exponent // 2
        base = (sumPowersOfEight(half) + offsetPrefixSum(half - 1)) % MODULUS
        powers = (sumPowersOfFour(half) - half) % MODULUS
        return (base + pow(4, half, MODULUS) + powers) % MODULUS

    half = (exponent - 1) // 2
    base = (sumPowersOfEight(half + 1) + offsetPrefixSum(half)) % MODULUS
    powers = (sumPowersOfFour(half) - half) % MODULUS
    return (base + powers) % MODULUS


def runTests():
    assert winningBlackboardSum(4) == 46
    assert winningBlackboardSum(12) == 54_532
    assert winningBlackboardSum(1_234) == 690_421_393


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningBlackboardSum(12_345_678)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
