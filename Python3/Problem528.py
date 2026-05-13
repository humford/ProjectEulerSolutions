import math
import time


MODULUS = 1_000_000_007


def binomialSmallK(n, k, modulus=None):
    if n < 0 or k < 0 or k > n:
        return 0

    if modulus is None:
        return math.comb(n, k)

    numerator = 1
    for offset in range(k):
        numerator = numerator * ((n - offset) % modulus) % modulus

    return numerator * pow(math.factorial(k), -1, modulus) % modulus


def constrainedSum(n, k, base, modulus=None):
    caps = [base ** index + 1 for index in range(1, k + 1)]
    total = 0

    for mask in range(1 << k):
        shift = 0
        bits = 0
        for index, cap in enumerate(caps):
            if mask & (1 << index):
                shift += cap
                bits += 1

        remaining = n - shift
        if remaining < 0:
            continue

        term = binomialSmallK(remaining + k, k, modulus)
        if bits % 2:
            total -= term
        else:
            total += term

    if modulus is None:
        return total

    return total % modulus


def targetConstrainedSum():
    total = 0
    for k in range(10, 16):
        total += constrainedSum(10 ** k, k, k, MODULUS)
    return total % MODULUS


def runTests():
    assert constrainedSum(14, 3, 2) == 135
    assert constrainedSum(200, 5, 3) == 12_949_440
    assert constrainedSum(1_000, 10, 5, MODULUS) == 624_839_075


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = targetConstrainedSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
