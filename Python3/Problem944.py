from math import isqrt
import time


TARGET = 10**14
MODULUS = 1_234_567_891


def triangularMod(n, modulus):
    if n % 2 == 0:
        return ((n // 2) % modulus) * ((n + 1) % modulus) % modulus
    return (n % modulus) * (((n + 1) // 2) % modulus) % modulus


def intervalSumMod(low, high, modulus):
    if low > high:
        return 0
    return (triangularMod(high, modulus) - triangularMod(low - 1, modulus)) % modulus


def S(n, modulus=MODULUS):
    common = pow(2, n - 1, modulus)
    total = common * triangularMod(n, modulus)

    root = isqrt(n)
    smallLimit = n // (root + 1)
    subtract = 0

    for x in range(1, smallLimit + 1):
        quotient = n // x
        subtract += (x % modulus) * pow(2, n - quotient, modulus)
        if x & 8191 == 0:
            subtract %= modulus

    inverseTwo = (modulus + 1) // 2
    power = common
    for quotient in range(1, root + 1):
        low = n // (quotient + 1) + 1
        high = n // quotient
        if low <= smallLimit:
            low = smallLimit + 1
        if low <= high:
            subtract += intervalSumMod(low, high, modulus) * power
            if quotient & 8191 == 0:
                subtract %= modulus
        power = (power * inverseTwo) % modulus

    return (total - subtract) % modulus


def runTests():
    assert S(10) == 4_927


def solve():
    return S(TARGET)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
