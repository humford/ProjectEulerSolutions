import time


PRIMES = (83, 89, 97)
POWER = 3


def extendedGcd(a, b):
    x0, y0 = 1, 0
    x1, y1 = 0, 1

    while b:
        quotient = a // b
        a, b = b, a - quotient * b
        x0, x1 = x1, x0 - quotient * x1
        y0, y1 = y1, y0 - quotient * y1

    return a, x0, y0


def modularInverse(a, modulus):
    gcdValue, x, _ = extendedGcd(a % modulus, modulus)
    if gcdValue != 1:
        raise ValueError("inverse does not exist")
    return x % modulus


def pAdicValuation(n, prime):
    if n == 0:
        return 10**18

    exponent = 0
    while n % prime == 0:
        n //= prime
        exponent += 1
    return exponent


def lastNonzeroFallingIndex(n, prime, power):
    """Largest j with v_p(n * (n - 1) * ... * (n - j + 1)) < power."""
    valuation = 0
    j = 0

    while valuation < power:
        j += 1
        if j > n:
            return n
        valuation += pAdicValuation(n - j + 1, prime)

    return j - 1


def forwardDifferencesOfPowers(n, maxIndex, modulus):
    values = [0] * (maxIndex + 1)
    if n == 0:
        values = [1] * (maxIndex + 1)
    else:
        for i in range(1, maxIndex + 1):
            values[i] = pow(i, n, modulus)

    differences = []
    for level in range(maxIndex + 1):
        differences.append(values[0] % modulus)
        for i in range(maxIndex - level):
            values[i] = (values[i + 1] - values[i]) % modulus

    return differences


def binomialPrefix(n, maxIndex, modulus):
    coefficients = [1 % modulus]
    coefficient = 1

    for j in range(1, maxIndex + 1):
        coefficient = coefficient * (n - j + 1) // j
        coefficients.append(coefficient % modulus)

    return coefficients


def solveModuloPrimePower(n, prime, power):
    modulus = prime**power
    maxIndex = min(n, lastNonzeroFallingIndex(n, prime, power))

    factoredStirling = forwardDifferencesOfPowers(n, maxIndex, modulus)
    binomialCoefficients = binomialPrefix(n, maxIndex, modulus)

    inverseTwo = modularInverse(2, modulus)
    powerOfTwo = pow(2, n, modulus)
    total = 0

    for j in range(maxIndex + 1):
        total += binomialCoefficients[j] * factoredStirling[j] * powerOfTwo
        total %= modulus
        powerOfTwo = powerOfTwo * inverseTwo % modulus

    return total


def chineseRemainder(residues, moduli):
    combinedModulus = 1
    for modulus in moduli:
        combinedModulus *= modulus

    result = 0
    for residue, modulus in zip(residues, moduli):
        partialModulus = combinedModulus // modulus
        inverse = modularInverse(partialModulus, modulus)
        result = (result + residue * partialModulus * inverse) % combinedModulus

    return result


def solve(n):
    moduli = [prime**POWER for prime in PRIMES]
    residues = [
        solveModuloPrimePower(n, prime, POWER)
        for prime in PRIMES
    ]
    return chineseRemainder(residues, moduli)


def runTests():
    assert solve(10) == 142469423360


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(10**18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
