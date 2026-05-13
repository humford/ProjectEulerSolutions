import math
import time


MOD_BITS = 48
MODULUS = 1 << MOD_BITS
ODD_PERIOD = 1 << (MOD_BITS - 1)
MAX_LOG_TERMS = 24
MAX_EXP_TERMS = 60


def v2(number):
    return (number & -number).bit_length() - 1


def smallCombination(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def stirlingSecondKind(maxN):
    values = [[0] * (maxN + 1) for _ in range(maxN + 1)]
    values[0][0] = 1
    for n in range(1, maxN + 1):
        for k in range(1, n + 1):
            values[n][k] = values[n - 1][k - 1] + k * values[n - 1][k]
    return values


STIRLING = stirlingSecondKind(MAX_LOG_TERMS)

FACTORIAL = [1] * (MAX_LOG_TERMS + 1)
for index in range(1, MAX_LOG_TERMS + 1):
    FACTORIAL[index] = FACTORIAL[index - 1] * index

BINOMIAL = [[0] * (MAX_LOG_TERMS + 1) for _ in range(MAX_LOG_TERMS + 1)]
for n in range(MAX_LOG_TERMS + 1):
    BINOMIAL[n][0] = 1
    BINOMIAL[n][n] = 1
    for k in range(1, n):
        BINOMIAL[n][k] = BINOMIAL[n - 1][k - 1] + BINOMIAL[n - 1][k]

FACTORIAL_V2 = [0] * (MAX_EXP_TERMS + 1)
FACTORIAL_ODD = [1] * (MAX_EXP_TERMS + 1)
for n in range(1, MAX_EXP_TERMS + 1):
    twos = v2(n)
    FACTORIAL_V2[n] = FACTORIAL_V2[n - 1] + twos
    FACTORIAL_ODD[n] = FACTORIAL_ODD[n - 1] * (n >> twos) % MODULUS

FACTORIAL_ODD_INVERSE = [pow(value, -1, MODULUS) for value in FACTORIAL_ODD]


def powerSumsUpto(n, maxPower=MAX_LOG_TERMS):
    combinations = [0] * (maxPower + 2)
    for k in range(1, maxPower + 2):
        combinations[k] = smallCombination(n, k) % MODULUS

    sums = [0] * (maxPower + 1)
    sums[0] = n % MODULUS
    for power in range(1, maxPower + 1):
        total = 0
        for t in range(power + 1):
            if STIRLING[power][t]:
                total += STIRLING[power][t] * FACTORIAL[t] * combinations[t + 1]
        sums[power] = total % MODULUS
    return sums


def expPrincipalUnit(value):
    value %= MODULUS
    result = 1
    powerValue = 1

    for n in range(1, MAX_EXP_TERMS + 1):
        powerValue *= value
        shift = FACTORIAL_V2[n]
        term = ((powerValue >> shift) % MODULUS) * FACTORIAL_ODD_INVERSE[n] % MODULUS
        result = (result + term) % MODULUS
        if term == 0:
            break

    return result


ODD_PRODUCT_CACHE = {0: 1}


def firstOddProduct(count):
    count %= ODD_PERIOD
    cached = ODD_PRODUCT_CACHE.get(count)
    if cached is not None:
        return cached

    signFlip = (count // 2) & 1
    evenCount = (count + 1) // 2
    oddCount = count // 2

    evenSums = powerSumsUpto(evenCount)
    oddSums = powerSumsUpto(oddCount)

    transformBase = (1 << (MOD_BITS - 2)) - 1
    transformPowers = [1] * (MAX_LOG_TERMS + 1)
    for index in range(1, MAX_LOG_TERMS + 1):
        transformPowers[index] = transformPowers[index - 1] * transformBase % MODULUS

    logSum = 0
    for power in range(1, MAX_LOG_TERMS + 1):
        oddTransformedSum = 0
        for t in range(power + 1):
            term = BINOMIAL[power][t] * transformPowers[power - t]
            if t & 1:
                term = -term
            oddTransformedSum = (oddTransformedSum + term * oddSums[t]) % MODULUS

        totalPowerSum = (evenSums[power] + oddTransformedSum) % MODULUS

        denominator = power
        twos = v2(denominator)
        oddPart = denominator >> twos
        coefficient = (1 << (2 * power - twos)) % MODULUS
        coefficient = coefficient * pow(oddPart, -1, MODULUS) % MODULUS
        if power % 2 == 0:
            coefficient = -coefficient % MODULUS

        logSum = (logSum + coefficient * totalPowerSum) % MODULUS

    result = expPrincipalUnit(logSum)
    if signFlip:
        result = -result % MODULUS

    ODD_PRODUCT_CACHE[count] = result
    return result


def oddProductUpTo(limit):
    return firstOddProduct((limit + 1) // 2)


def oddPartFactorial(limit):
    result = 1
    while limit:
        result = result * oddProductUpTo(limit) % MODULUS
        limit //= 2
    return result


def trailingHexDigits(limit):
    oddPart = oddPartFactorial(limit)
    v2Mod4 = (limit - limit.bit_count()) & 3
    value = oddPart * (1 << v2Mod4) % MODULUS
    return format(value, "012X")


def factorial(limit):
    result = 1
    for number in range(2, limit + 1):
        result *= number
    return result


def targetTrailingHexDigits():
    return trailingHexDigits(factorial(20))


def runTests():
    assert trailingHexDigits(20) == "21C3677C82B4"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = targetTrailingHexDigits()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
