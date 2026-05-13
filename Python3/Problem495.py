import math
import time
from array import array


MODULUS = 1_000_000_007


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


def factorization(n):
    factors = {}
    factor = 2

    while factor * factor <= n:
        while n % factor == 0:
            factors[factor] = factors.get(factor, 0) + 1
            n //= factor
        factor += 1 if factor == 2 else 2

    if n > 1:
        factors[n] = factors.get(n, 0) + 1

    return factors


def factorialPrimeExponentFrequencies(limit):
    frequencies = {}

    for prime in primeSieve(limit):
        exponent = 0
        quotient = limit
        while quotient:
            quotient //= prime
            exponent += quotient
        frequencies[exponent] = frequencies.get(exponent, 0) + 1

    return frequencies


def integerPartitions(n, maxPart=None):
    if maxPart is None or maxPart > n:
        maxPart = n
    if n == 0:
        yield []
        return

    for first in range(maxPart, 0, -1):
        for rest in integerPartitions(n - first, first):
            yield [first] + rest


def precomputeOneTwoCycleCoefficients(maxExponent, k):
    inverses = [0] * (maxExponent + 1)
    if maxExponent >= 1:
        inverses[1] = 1
        for value in range(2, maxExponent + 1):
            inverses[value] = (
                MODULUS - (MODULUS // value) * inverses[MODULUS % value] % MODULUS
            )

    oneCycle = [None] * (k + 1)
    oneCycle[0] = [0] * (maxExponent + 1)
    oneCycle[0][0] = 1
    for count in range(1, k + 1):
        coefficients = [0] * (maxExponent + 1)
        coefficients[0] = 1
        for exponent in range(1, maxExponent + 1):
            coefficients[exponent] = (
                coefficients[exponent - 1]
                * (count + exponent - 1)
                % MODULUS
                * inverses[exponent]
                % MODULUS
            )
        oneCycle[count] = coefficients

    base = [[None] * (k // 2 + 1) for _ in range(k + 1)]
    for ones in range(k + 1):
        base[ones][0] = array("I", oneCycle[ones])
        for twos in range(1, k // 2 + 1):
            coefficients = list(base[ones][twos - 1])
            for exponent in range(2, maxExponent + 1):
                value = coefficients[exponent] + coefficients[exponent - 2]
                if value >= MODULUS:
                    value -= MODULUS
                coefficients[exponent] = value
            base[ones][twos] = array("I", coefficients)

    return base


def productPartitionsFromExponentFrequencies(frequencies, k):
    if k == 0:
        return 1

    exponentData = sorted(frequencies.items())
    maxExponent = exponentData[-1][0] if exponentData else 0

    factorials = [1] * (k + 1)
    for value in range(1, k + 1):
        factorials[value] = factorials[value - 1] * value % MODULUS

    inverseFactorials = [1] * (k + 1)
    inverseFactorials[k] = pow(factorials[k], MODULUS - 2, MODULUS)
    for value in range(k, 0, -1):
        inverseFactorials[value - 1] = inverseFactorials[value] * value % MODULUS

    inversePowers = [[1] * (k + 1) for _ in range(k + 1)]
    for cycleLength in range(1, k + 1):
        inverseCycleLength = pow(cycleLength, MODULUS - 2, MODULUS)
        accumulator = 1
        for count in range(1, k + 1):
            accumulator = accumulator * inverseCycleLength % MODULUS
            inversePowers[cycleLength][count] = accumulator

    oneTwoBase = precomputeOneTwoCycleCoefficients(maxExponent, k)
    total = 0

    for partition in integerPartitions(k):
        cycleCount = len(partition)
        ones = twos = 0
        index = cycleCount - 1

        while index >= 0 and partition[index] == 1:
            ones += 1
            index -= 1
        while index >= 0 and partition[index] == 2:
            twos += 1
            index -= 1

        if ones == 0 and frequencies.get(1, 0):
            continue

        coefficients = list(oneTwoBase[ones][twos])
        for cycleLength in partition[:index + 1]:
            for exponent in range(cycleLength, maxExponent + 1):
                value = coefficients[exponent] + coefficients[exponent - cycleLength]
                if value >= MODULUS:
                    value -= MODULUS
                coefficients[exponent] = value

        fixedTupleCount = 1
        for exponent, frequency in exponentData:
            coefficient = coefficients[exponent]
            if coefficient == 0:
                fixedTupleCount = 0
                break
            fixedTupleCount = fixedTupleCount * pow(coefficient, frequency, MODULUS) % MODULUS

        if fixedTupleCount == 0:
            continue

        cycleWeight = 1
        start = 0
        while start < cycleCount:
            cycleLength = partition[start]
            stop = start + 1
            while stop < cycleCount and partition[stop] == cycleLength:
                stop += 1

            repeated = stop - start
            cycleWeight = cycleWeight * inversePowers[cycleLength][repeated] % MODULUS
            cycleWeight = cycleWeight * inverseFactorials[repeated] % MODULUS
            start = stop

        if (k - cycleCount) % 2:
            cycleWeight = MODULUS - cycleWeight

        total = (total + cycleWeight * fixedTupleCount) % MODULUS

    return total


def productPartitions(n, k):
    exponentFrequencies = {}
    for exponent in factorization(n).values():
        exponentFrequencies[exponent] = exponentFrequencies.get(exponent, 0) + 1
    return productPartitionsFromExponentFrequencies(exponentFrequencies, k)


def factorialProductPartitions(limit, k):
    return productPartitionsFromExponentFrequencies(
        factorialPrimeExponentFrequencies(limit),
        k,
    )


def runTests():
    assert productPartitions(144, 4) == 7
    assert factorialProductPartitions(100, 10) == 287_549_200


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = factorialProductPartitions(10_000, 30)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
