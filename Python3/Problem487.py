import math
import time


def powerPrefixSum(k, n):
    return sum(sum(value ** k for value in range(1, end + 1)) for end in range(1, n + 1))


def primeSieve(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start:limit + 1:number] = b"\x00" * ((limit - start) // number + 1)

    return [number for number in range(limit + 1) if sieve[number]]


def intervalPrimes(start, stop):
    smallPrimes = primeSieve(math.isqrt(stop) + 1)
    primes = []

    for candidate in range(start, stop + 1):
        if candidate < 2:
            continue

        isPrime = True
        for prime in smallPrimes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                isPrime = candidate == prime
                break

        if isPrime:
            primes.append(candidate)

    return primes


def inverseFactorials(limit, modulus):
    factorials = [1] * (limit + 1)
    for value in range(1, limit + 1):
        factorials[value] = factorials[value - 1] * value % modulus

    inverseFactorials = [1] * (limit + 1)
    inverseFactorials[limit] = pow(factorials[limit], modulus - 2, modulus)
    for value in range(limit, 0, -1):
        inverseFactorials[value - 1] = inverseFactorials[value] * value % modulus

    return inverseFactorials


def lagrangeEvaluateZeroToDegree(values, argument, degree, modulus, inverseFactorials):
    if argument <= degree:
        return values[argument]

    prefix = [1] * (degree + 2)
    for index in range(degree + 1):
        prefix[index + 1] = prefix[index] * (argument - index) % modulus

    suffix = [1] * (degree + 2)
    for index in range(degree, -1, -1):
        suffix[index] = suffix[index + 1] * (argument - index) % modulus

    total = 0
    for index in range(degree + 1):
        numerator = prefix[index] * suffix[index + 1] % modulus
        term = values[index] * numerator % modulus
        term = term * inverseFactorials[index] % modulus
        term = term * inverseFactorials[degree - index] % modulus

        if (degree - index) % 2:
            total -= term
        else:
            total += term

    return total % modulus


def prefixPowerSums(k, degreeK, degreeKPlusOne, modulus):
    powerK = [0] * (degreeK + 1)
    powerKPlusOne = [0] * (degreeKPlusOne + 1)
    sumK = 0
    sumKPlusOne = 0

    for value in range(1, degreeKPlusOne + 1):
        kthPower = pow(value, k, modulus)
        sumK = (sumK + kthPower) % modulus
        if value <= degreeK:
            powerK[value] = sumK

        sumKPlusOne = (sumKPlusOne + kthPower * value) % modulus
        powerKPlusOne[value] = sumKPlusOne

    return powerK, powerKPlusOne


def powerPrefixSumModPrime(k, n, prime):
    degreeK = k + 1
    degreeKPlusOne = k + 2
    reducedN = n % prime

    inverseFacts = inverseFactorials(degreeKPlusOne, prime)
    powerK, powerKPlusOne = prefixPowerSums(k, degreeK, degreeKPlusOne, prime)

    fk = lagrangeEvaluateZeroToDegree(powerK, reducedN, degreeK, prime, inverseFacts)
    fkPlusOne = lagrangeEvaluateZeroToDegree(
        powerKPlusOne,
        reducedN,
        degreeKPlusOne,
        prime,
        inverseFacts,
    )

    return (((n + 1) % prime) * fk - fkPlusOne) % prime


def primeModPowerSum(k, n):
    total = 0
    for prime in intervalPrimes(2_000_000_000, 2_000_002_000):
        total += powerPrefixSumModPrime(k, n, prime)
    return total


def runTests():
    assert sum(value ** 2 for value in range(1, 11)) == 385
    assert powerPrefixSum(4, 100) == 35_375_333_830
    assert powerPrefixSumModPrime(4, 100, 101) == powerPrefixSum(4, 100) % 101


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeModPowerSum(10_000, 10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
