import math
import time
from array import array


P = 10_000_019
MOD = P * P


def cycleIndependenceCoefficients(n):
    coefficients = [0] * (n // 2 + 1)
    coefficients[0] = 1

    for r in range(1, n // 2 + 1):
        coefficients[r] = n * math.comb(n - r, r) // (n - r)

    return coefficients


def LSmall(n, k):
    row = cycleIndependenceCoefficients(n)
    total = [1]

    for _ in range(n):
        nextTotal = [0] * min(k + 1, len(total) + len(row) - 1)
        for i, a in enumerate(total):
            if not a:
                continue
            for j, b in enumerate(row):
                if i + j > k:
                    break
                nextTotal[i + j] += a * b
        total = nextTotal

    return total[k] if k < len(total) else 0


def precomputeModData():
    inversesP = array("I", [0]) * P
    inversesP[1] = 1
    for n in range(2, P):
        inversesP[n] = (P - (P // n) * inversesP[P % n] % P) % P

    factorial = array("Q", [0]) * P
    value = 1
    factorial[0] = 1
    for n in range(1, P):
        value = value * n % MOD
        factorial[n] = value

    harmonic = array("I", [0]) * P
    value = 0
    for n in range(1, P):
        value = (value + inversesP[n]) % P
        harmonic[n] = value

    return inversesP, factorial, harmonic


def solve():
    N = 10 ** 9
    K = 10 ** 15
    maxT = K // N

    inversesP, factorial, harmonic = precomputeModData()
    wilsonQuotient = ((factorial[P - 1] + 1) // P) % P

    def inverseModP2(value):
        value %= MOD
        inverse = inversesP[value % P]
        return inverse * (2 - value * inverse % MOD) % MOD

    def blockFactorialPower(blocks):
        result = (1 - (blocks % P) * P % MOD * wilsonQuotient % MOD) % MOD
        if blocks & 1:
            result = (-result) % MOD
        return result

    def unitFactorial(n):
        result = 1
        while n:
            blocks, rest = divmod(n, P)
            result = result * factorial[rest] % MOD
            result = result * (1 + (blocks % P) * harmonic[rest] % P * P) % MOD
            result = result * blockFactorialPower(blocks) % MOD
            n = blocks
        return result

    def primeValuationFactorial(n):
        quotient = n // P
        return quotient + quotient // P

    def binomialModP2(n, k):
        if k < 0 or k > n:
            return 0

        exponent = (
            primeValuationFactorial(n)
            - primeValuationFactorial(k)
            - primeValuationFactorial(n - k)
        )
        if exponent >= 2:
            return 0

        value = unitFactorial(n)
        value = value * inverseModP2(unitFactorial(k)) % MOD
        value = value * inverseModP2(unitFactorial(n - k)) % MOD
        if exponent == 1:
            value = value * P % MOD

        return value

    def alphaPowerCoefficient(power, degree):
        if degree == 0:
            return 1

        value = binomialModP2(power - degree - 1, degree - 1)
        return power % MOD * inverseModP2(degree) % MOD * value % MOD

    choose = 1
    answer = 0
    degree = K
    alphaPower = N * N

    for t in range(maxT + 1):
        if t:
            choose = choose * ((N - t + 1) % MOD) % MOD
            choose = choose * inverseModP2(t) % MOD

        answer = (answer + choose * alphaPowerCoefficient(alphaPower, degree)) % MOD
        degree -= N
        alphaPower -= 2 * N

    return answer


def runTests():
    assert LSmall(2, 2) == 4
    assert LSmall(6, 12) == 4_204_761


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
