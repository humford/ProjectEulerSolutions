import time


MOD = 1_000_000_007


def factorialTables(limit, modulus=MOD):
    factorial = [1] * (limit + 1)
    for n in range(1, limit + 1):
        factorial[n] = factorial[n - 1] * n % modulus

    inverseFactorial = [1] * (limit + 1)
    inverseFactorial[limit] = pow(factorial[limit], modulus - 2, modulus)
    for n in range(limit, 0, -1):
        inverseFactorial[n - 1] = inverseFactorial[n] * n % modulus

    return factorial, inverseFactorial


def binomial(n, k, factorial, inverseFactorial, modulus=MOD):
    if k < 0 or k > n:
        return 0
    return factorial[n] * inverseFactorial[k] * inverseFactorial[n - k] % modulus


def D(N, modulus=MOD):
    factorial, inverseFactorial = factorialTables(N, modulus)
    powers9 = [1] * (N + 2)
    for n in range(1, N + 2):
        powers9[n] = powers9[n - 1] * 9 % modulus

    total = 0
    for length in range(1, N + 1):
        for count in range(length // 2 + 1, length + 1):
            total += binomial(length, count, factorial, inverseFactorial, modulus) * powers9[length - count + 1]
            total %= modulus
    return total


def isDominating(n):
    digits = str(n)
    return max(digits.count(digit) for digit in set(digits)) * 2 > len(digits)


def runTests():
    assert isDominating(2022)
    assert not isDominating(2021)
    assert D(4) == 603
    assert D(10) == 21_893_256


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = D(2022)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
