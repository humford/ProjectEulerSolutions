import time
from array import array


MOD = 1_000_000_007


def factorialTables(limit):
    factorial = array("I", [1]) * (limit + 1)
    for n in range(2, limit + 1):
        factorial[n] = factorial[n - 1] * n % MOD

    inverseFactorial = array("I", [1]) * (limit + 1)
    inverseFactorial[limit] = pow(int(factorial[limit]), MOD - 2, MOD)
    for n in range(limit, 0, -1):
        inverseFactorial[n - 1] = inverseFactorial[n] * n % MOD

    return factorial, inverseFactorial


def binomial(n, k, factorial, inverseFactorial):
    if k < 0 or k > n:
        return 0
    return int(factorial[n]) * int(inverseFactorial[k]) % MOD * int(inverseFactorial[n - k]) % MOD


def fwhtXor(values):
    length = len(values)
    half = 1
    while half < length:
        step = 2 * half
        for start in range(0, length, step):
            for i in range(start, start + half):
                x = int(values[i])
                y = int(values[i + half])
                u = x + y
                if u >= MOD:
                    u -= MOD
                v = x - y
                if v < 0:
                    v += MOD
                values[i] = u
                values[i + half] = v
        half = step


def singleSuitDistributionPadded(n, length):
    distribution = array("I", [0]) * length
    if n <= 0:
        return distribution
    if n == 1:
        distribution[0] = 2
        return distribution

    factorial, inverseFactorial = factorialTables(n)

    distribution[0] = (pow(2, n - 2, MOD) + 2) % MOD
    distribution[1] = (pow(2, n - 2, MOD) + n - 2) % MOD
    if n > 2:
        distribution[2] = (pow(2, n - 3, MOD) + n - 3) % MOD

    inverse4 = pow(4, MOD - 2, MOD)

    def Q(X, k):
        n1 = X + k + 1
        return (
            X * binomial(n1, k + 1, factorial, inverseFactorial)
            - (k + 1) * binomial(n1, k + 2, factorial, inverseFactorial)
        ) % MOD

    def fillParity(startGrundy, startX):
        if startGrundy >= n or startX < 0:
            return

        k = 0
        X = startX
        F = (pow(2, X + 1, MOD) - 1) % MOD

        while True:
            grundy = 2 * k + startGrundy
            if grundy >= n or X < 0:
                break
            distribution[grundy] = (F + Q(X, k)) % MOD

            if X < 2:
                break

            c1 = binomial(X + k - 1, k, factorial, inverseFactorial)
            c2 = binomial(X + k, k, factorial, inverseFactorial)
            previousF = (F - 2 * c1 - c2) % MOD
            previousF = previousF * inverse4 % MOD
            cNext = binomial(X + k - 1, k + 1, factorial, inverseFactorial)
            F = (2 * previousF - cNext) % MOD

            k += 1
            X -= 2

    fillParity(3, n - 4)
    fillParity(4, n - 5)

    return distribution


def C(n, suits):
    if n == 0:
        return 1

    length = 1 << (n - 1).bit_length()
    distribution = singleSuitDistributionPadded(n, length)
    fwhtXor(distribution)

    total = 0
    for index, value in enumerate(distribution):
        total += pow(int(value), suits, MOD)
        if index % 8192 == 0:
            total %= MOD
    total %= MOD

    return total * pow(length, MOD - 2, MOD) % MOD


def runTests():
    assert C(3, 2) == 26
    assert C(13, 4) == 540_318_329


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = C(10_000_000, 10_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
