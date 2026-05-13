import time


MOD = 1_000_000_007


def primeSieve(limit):
    if limit < 2:
        return []

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for p in range(2, int(limit**0.5) + 1):
        if isPrime[p]:
            isPrime[p * p:limit + 1:p] = b"\x00" * (((limit - p * p) // p) + 1)

    return [n for n in range(2, limit + 1) if isPrime[n]]


def factorizeSmall(n, primes):
    factors = {}
    value = n

    for prime in primes:
        if prime * prime > value:
            break
        if value % prime == 0:
            exponent = 0
            while value % prime == 0:
                value //= prime
                exponent += 1
            factors[prime] = exponent

    if value > 1:
        factors[value] = factors.get(value, 0) + 1

    return factors


def factorialPrimeExponents(n, primes):
    exponents = {}
    for prime in primes:
        if prime > n:
            break
        exponent = 0
        value = n
        while value:
            value //= prime
            exponent += value
        exponents[prime] = exponent
    return exponents


def inverseTable(n, modulus):
    inverses = [0] * (n + 1)
    inverses[1] = 1
    for value in range(2, n + 1):
        inverses[value] = modulus - (modulus // value) * inverses[modulus % value] % modulus
    return inverses


def sigmaPowerFromExponents(exponents, power, modulus):
    result = 1

    for prime, exponent in exponents.items():
        primePower = pow(prime, power, modulus)
        if primePower == 1:
            term = (exponent + 1) % modulus
        else:
            term = (pow(primePower, exponent + 1, modulus) - 1) % modulus
            term = term * pow((primePower - 1) % modulus, modulus - 2, modulus) % modulus
        result = result * term % modulus

    return result


def nModFromExponents(exponents, modulus):
    result = 1
    for prime, exponent in exponents.items():
        result = result * pow(prime, exponent, modulus) % modulus
    return result


def sigmaData(exponents, modulus):
    nMod = nModFromExponents(exponents, modulus)
    sigma = {}
    for power in (1, 3, 5, 7, 9, 11):
        sigma[power] = sigmaPowerFromExponents(exponents, power, modulus)
    return nMod, sigma


def sigma1UpTo(limit):
    sigma = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            sigma[multiple] += divisor
    return sigma


def tauUpTo(limit, modulus):
    sigma1 = sigma1UpTo(limit)
    inverses = inverseTable(limit, modulus)
    tau = [0] * (limit + 1)
    tau[1] = 1

    for k in range(2, limit + 1):
        total = 0
        for m in range(1, k):
            total += sigma1[m] * tau[k - m]
        tau[k] = (-24 * (total % modulus)) % modulus
        tau[k] = tau[k] * inverses[k - 1] % modulus

    return tau


def multiplyMatrices(left, right, modulus):
    a, b, c, d = left
    e, f, g, h = right
    return (
        (a * e + b * g) % modulus,
        (a * f + b * h) % modulus,
        (c * e + d * g) % modulus,
        (c * f + d * h) % modulus,
    )


def tauPrimePower(prime, exponent, tauPrime, modulus):
    if exponent == 0:
        return 1
    if exponent == 1:
        return tauPrime % modulus

    prime11 = pow(prime, 11, modulus)
    matrix = (tauPrime % modulus, (-prime11) % modulus, 1, 0)
    result = (1, 0, 0, 1)
    power = exponent - 1

    while power:
        if power % 2:
            result = multiplyMatrices(result, matrix, modulus)
        matrix = multiplyMatrices(matrix, matrix, modulus)
        power //= 2

    a, b, _c, _d = result
    return (a * (tauPrime % modulus) + b) % modulus


def tauFromExponents(exponents, tauValues, modulus):
    result = 1
    for prime, exponent in exponents.items():
        result = result * tauPrimePower(prime, exponent, tauValues[prime], modulus) % modulus
    return result


INV_691 = pow(691, MOD - 2, MOD)
E_COEFFICIENT = {
    2: (-24) % MOD,
    4: 240 % MOD,
    6: (-504) % MOD,
    8: 480 % MOD,
    10: (-264) % MOD,
    12: 65520 * INV_691 % MOD,
}


def coefficientEk(weight, sigma):
    if weight == 2:
        return E_COEFFICIENT[2] * sigma[1] % MOD
    return E_COEFFICIENT[weight] * sigma[weight - 1] % MOD


def coefficientDerivativeEk(weight, derivativeOrder, nPowers, sigma):
    return nPowers[derivativeOrder] * coefficientEk(weight, sigma) % MOD


INV2 = (MOD + 1) // 2
INV5 = pow(5, MOD - 2, MOD)
INV7 = pow(7, MOD - 2, MOD)
INV24185 = pow(24185, MOD - 2, MOD)


def coefficientE2Power(power, nPowers, sigma, tauValue):
    if power == 1:
        return coefficientEk(2, sigma)
    if power == 2:
        return (coefficientEk(4, sigma) + 12 * coefficientDerivativeEk(2, 1, nPowers, sigma)) % MOD
    if power == 3:
        return (
            coefficientEk(6, sigma)
            + 9 * coefficientDerivativeEk(4, 1, nPowers, sigma)
            + 72 * coefficientDerivativeEk(2, 2, nPowers, sigma)
        ) % MOD
    if power == 4:
        return (
            coefficientEk(8, sigma)
            + 8 * coefficientDerivativeEk(6, 1, nPowers, sigma)
            + (216 * INV5 % MOD) * coefficientDerivativeEk(4, 2, nPowers, sigma)
            + 288 * coefficientDerivativeEk(2, 3, nPowers, sigma)
        ) % MOD
    if power == 5:
        return (
            coefficientEk(10, sigma)
            + (15 * INV2 % MOD) * coefficientDerivativeEk(8, 1, nPowers, sigma)
            + (240 * INV7 % MOD) * coefficientDerivativeEk(6, 2, nPowers, sigma)
            + 144 * coefficientDerivativeEk(4, 3, nPowers, sigma)
            + 864 * coefficientDerivativeEk(2, 4, nPowers, sigma)
        ) % MOD
    if power == 6:
        return (
            coefficientEk(12, sigma)
            + ((-4608) % MOD) * INV24185 % MOD * tauValue
            + (36 * INV5 % MOD) * coefficientDerivativeEk(10, 1, nPowers, sigma)
            + 30 * coefficientDerivativeEk(8, 2, nPowers, sigma)
            + (720 * INV7 % MOD) * coefficientDerivativeEk(6, 3, nPowers, sigma)
            + (2592 * INV7 % MOD) * coefficientDerivativeEk(4, 4, nPowers, sigma)
            + (10368 * INV5 % MOD) * coefficientDerivativeEk(2, 5, nPowers, sigma)
        ) % MOD

    raise ValueError("power must be between 1 and 6")


def smallCombination(n, k):
    if k < 0 or k > n:
        return 0
    if k > n - k:
        k = n - k

    numerator = 1
    denominator = 1
    for value in range(1, k + 1):
        numerator *= n - (k - value)
        denominator *= value
    return numerator // denominator


def powersOfN(nMod, maxPower):
    powers = [1]
    for _ in range(maxPower):
        powers.append(powers[-1] * nMod % MOD)
    return powers


def RDimensionAtN(dimension, nPowers, sigma, tauValue):
    inverse12 = pow(12, MOD - 2, MOD)
    scale = pow(inverse12, dimension, MOD)
    total = 0

    for power in range(1, dimension + 1):
        term = smallCombination(dimension, power) * coefficientE2Power(power, nPowers, sigma, tauValue)
        term %= MOD
        if power % 2:
            total = (total - term) % MOD
        else:
            total = (total + term) % MOD

    return total * scale % MOD


def prepareInput(exponents):
    nMod, sigma = sigmaData(exponents, MOD)
    return powersOfN(nMod, 5), sigma


def runTests(primes, tauValues):
    ex10 = factorizeSmall(10, primes)
    nPowers10, sigma10 = prepareInput(ex10)
    assert RDimensionAtN(1, nPowers10, sigma10, 0) == 36

    ex100 = factorizeSmall(100, primes)
    nPowers100, sigma100 = prepareInput(ex100)
    assert RDimensionAtN(2, nPowers100, sigma100, 0) == 1_873_044

    ex100Factorial = factorialPrimeExponents(100, primes)
    nPowers100Factorial, sigma100Factorial = prepareInput(ex100Factorial)
    assert RDimensionAtN(2, nPowers100Factorial, sigma100Factorial, 0) == 446_575_636


def solve():
    primes = primeSieve(10_000)
    tauValues = tauUpTo(10_000, MOD)
    runTests(primes, tauValues)

    exponents = factorialPrimeExponents(10_000, primes)
    nPowers, sigma = prepareInput(exponents)
    tauValue = tauFromExponents(exponents, tauValues, MOD)
    return RDimensionAtN(6, nPowers, sigma, tauValue)


if __name__ == "__main__":
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
