import functools
import math
import time
from array import array

import numpy


DIVISOR_TABLE_LIMIT = 10_000_000
VECTOR_CHUNK_SIZE = 2_000_000


def _f(n):
    total = 0
    for divisor in range(1, math.isqrt(n) + 1):
        if n % divisor == 0:
            other = n // divisor
            value = math.gcd(divisor, other)
            total += value
            if divisor != other:
                total += value
    return total


@functools.cache
def totientPrefix(limit):
    phi = array("I", [0]) * (limit + 1)
    composite = bytearray(limit + 1)
    primes = []
    if limit >= 1:
        phi[1] = 1

    for number in range(2, limit + 1):
        if not composite[number]:
            primes.append(number)
            phi[number] = number - 1

        for prime in primes:
            product = number * prime
            if product > limit:
                break

            composite[product] = 1
            if number % prime == 0:
                phi[product] = phi[number] * prime
                break
            phi[product] = phi[number] * (prime - 1)

    prefix = array("Q", [0]) * (limit + 1)
    total = 0
    for number in range(1, limit + 1):
        total += phi[number]
        prefix[number] = total

    return prefix


@functools.cache
def divisorSummatoryTable(limit):
    divisorCounts = array("I", [0]) * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            divisorCounts[multiple] += 1

    prefix = array("Q", [0]) * (limit + 1)
    total = 0
    for number in range(1, limit + 1):
        total += divisorCounts[number]
        prefix[number] = total

    return prefix


def divisorSummatory(n, table):
    if n < len(table):
        return table[n]

    root = math.isqrt(n)
    halfTotal = 0
    for start in range(1, root + 1, VECTOR_CHUNK_SIZE):
        end = min(root + 1, start + VECTOR_CHUNK_SIZE)
        divisors = numpy.arange(start, end, dtype=numpy.int64)
        halfTotal += int((n // divisors).sum())

    return 2 * halfTotal - root * root


def gcdDivisorSum(limit):
    root = math.isqrt(limit)
    phiPrefix = totientPrefix(root)
    divisorTable = divisorSummatoryTable(min(DIVISOR_TABLE_LIMIT, limit))

    total = 0
    start = 1
    while start <= root:
        quotient = limit // (start * start)
        end = math.isqrt(limit // quotient)
        totientSum = phiPrefix[end] - phiPrefix[start - 1]
        total += totientSum * divisorSummatory(quotient, divisorTable)
        start = end + 1

    return total


def runTests():
    assert sum(_f(n) for n in range(1, 11)) == 32
    assert gcdDivisorSum(10) == 32
    assert gcdDivisorSum(1_000) == 12_776


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gcdDivisorSum(10 ** 15)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
