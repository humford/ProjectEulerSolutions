import math
import time
from array import array


MODULUS = 1_000_000_007


def primesUpTo(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)

    return [number for number in range(2, limit + 1) if sieve[number]]


def primesInOpenInterval(lower, upper):
    start = lower + 1
    length = upper - start
    if length <= 0:
        return

    segment = bytearray(b"\x01") * length
    for offset in range(max(0, 2 - start)):
        segment[offset] = 0

    for prime in primesUpTo(math.isqrt(upper - 1)):
        firstMultiple = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if firstMultiple < upper:
            segment[firstMultiple - start : length : prime] = b"\x00" * (
                ((upper - 1 - firstMultiple) // prime) + 1
            )

    for offset, isPrime in enumerate(segment):
        if isPrime:
            yield start + offset


def buildFactorials(limit):
    factorials = array("I", [1]) * (limit + 1)
    inverseFactorials = array("I", [1]) * (limit + 1)

    for number in range(1, limit + 1):
        factorials[number] = factorials[number - 1] * number % MODULUS

    inverseFactorials[limit] = pow(factorials[limit], MODULUS - 2, MODULUS)
    for number in range(limit, 0, -1):
        inverseFactorials[number - 1] = inverseFactorials[number] * number % MODULUS

    return factorials, inverseFactorials


def binomialMod(n, k, factorials, inverseFactorials):
    if k < 0 or k > n:
        return 0
    return factorials[n] * inverseFactorials[k] % MODULUS * inverseFactorials[n - k] % MODULUS


def ceilMultipleSqrt(multiplier, number):
    root = math.isqrt(number)
    if root * root == number:
        return multiplier * root
    return math.isqrt(multiplier * multiplier * number) + 1


def realRecursion(n, factorials=None, inverseFactorials=None):
    if factorials is None or inverseFactorials is None:
        factorials, inverseFactorials = buildFactorials(n + math.isqrt(n) + 2)

    rootStepsLimit = math.isqrt(n)
    total = 0

    # A path contributes only when its final subtraction is the first one that
    # leaves a value below sqrt(n).  Count paths ending in a sqrt(n)-step and
    # paths ending in a 1-step separately.
    for rootSteps in range(1, rootStepsLimit + 1):
        lowerOnes = n - ceilMultipleSqrt(rootSteps + 1, n) + 1
        upperOnes = n - ceilMultipleSqrt(rootSteps, n)
        if lowerOnes <= upperOnes:
            total += binomialMod(upperOnes + rootSteps, rootSteps, factorials, inverseFactorials)
            total -= binomialMod(lowerOnes + rootSteps - 1, rootSteps, factorials, inverseFactorials)
            total %= MODULUS

    for rootSteps in range(rootStepsLimit + 1):
        ones = n - ceilMultipleSqrt(rootSteps + 1, n) + 1
        if ones >= 1:
            total += binomialMod(ones + rootSteps - 1, rootSteps, factorials, inverseFactorials)
            total %= MODULUS

    return total


def primeRealRecursionSum(lower, upper):
    factorialLimit = upper + math.isqrt(upper) + 2
    factorials, inverseFactorials = buildFactorials(factorialLimit)

    total = 0
    for prime in primesInOpenInterval(lower, upper):
        total += realRecursion(prime, factorials, inverseFactorials)
        total %= MODULUS
    return total


def runTests():
    assert realRecursion(90) == 7_564_511


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeRealRecursionSum(10_000_000, 10_010_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
