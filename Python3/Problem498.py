import math
import time


MODULUS = 999_999_937


def signedCoefficient(n, m, d):
    if d < 0 or d >= m:
        return 0

    secondTop = n - d - 1
    secondBottom = m - d - 1
    if secondBottom < 0 or secondBottom > secondTop:
        return 0

    sign = -1 if (m - 1 - d) % 2 else 1
    return sign * math.comb(n, d) * math.comb(secondTop, secondBottom)


def maxLucasDigit(pairs, prime):
    maximum = 0
    for n, k in pairs:
        while n or k:
            maximum = max(maximum, n % prime)
            n //= prime
            k //= prime
    return maximum


def factorialTables(limit, prime):
    factorials = [1] * (limit + 1)
    for value in range(1, limit + 1):
        factorials[value] = factorials[value - 1] * value % prime

    inverseFactorials = [1] * (limit + 1)
    inverseFactorials[limit] = pow(factorials[limit], prime - 2, prime)
    for value in range(limit, 0, -1):
        inverseFactorials[value - 1] = inverseFactorials[value] * value % prime

    return factorials, inverseFactorials


def binomialLucas(n, k, prime, factorials, inverseFactorials):
    result = 1

    while n or k:
        nDigit = n % prime
        kDigit = k % prime
        if kDigit > nDigit:
            return 0

        result *= factorials[nDigit]
        result %= prime
        result *= inverseFactorials[kDigit]
        result %= prime
        result *= inverseFactorials[nDigit - kDigit]
        result %= prime

        n //= prime
        k //= prime

    return result


def coefficient(n, m, d, modulus=None):
    if modulus is None:
        return abs(signedCoefficient(n, m, d))

    pairs = [(n, d), (n - d - 1, m - d - 1)]
    maxDigit = maxLucasDigit(pairs, modulus)
    factorials, inverseFactorials = factorialTables(maxDigit, modulus)

    first = binomialLucas(n, d, modulus, factorials, inverseFactorials)
    second = binomialLucas(n - d - 1, m - d - 1, modulus, factorials, inverseFactorials)
    return first * second % modulus


def runTests():
    assert signedCoefficient(6, 3, 0) == 10
    assert signedCoefficient(6, 3, 1) == -24
    assert signedCoefficient(6, 3, 2) == 15
    assert coefficient(6, 3, 1) == 24
    assert coefficient(100, 10, 4) == 227_197_811_615_775


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = coefficient(10 ** 13, 10 ** 12, 10 ** 4, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
