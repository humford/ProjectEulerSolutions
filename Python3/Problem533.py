import math
import time

import numpy


MODULUS = 10 ** 9


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )
    return sieve


def applyIncrementalCarmichaelFactors(threshold, callback):
    primes = primeSieve(threshold)

    callback(1, 2)
    if threshold > 2:
        callback(2, 2)
        callback(2, 2)

        contribution = 4
        while contribution < threshold:
            callback(contribution, 2)
            contribution *= 2

    for prime in range(3, threshold + 1, 2):
        if not primes[prime]:
            continue

        contribution = prime - 1
        while contribution < threshold:
            callback(contribution, prime)
            contribution *= prime


def bestCarmichaelValueBelow(threshold):
    scores = numpy.zeros(threshold, dtype=numpy.float64)

    def addScore(contribution, prime):
        scores[contribution::contribution] += math.log(prime)

    applyIncrementalCarmichaelFactors(threshold, addScore)
    bestValue = int(scores[1:].argmax() + 1)

    topTwo = numpy.argpartition(scores[1:], -2)[-2:] + 1
    topTwo = topTwo[numpy.argsort(scores[topTwo])]
    assert scores[topTwo[-1]] - scores[topTwo[-2]] > 1e-6

    return bestValue


def largestNumberWithSmallCarmichael(threshold):
    bestValue = bestCarmichaelValueBelow(threshold)
    result = 1

    def multiplyIfAllowed(contribution, prime):
        nonlocal result
        if bestValue % contribution == 0:
            result *= prime

    applyIncrementalCarmichaelFactors(threshold, multiplyIfAllowed)
    return result


def carmichaelThreshold(threshold):
    return largestNumberWithSmallCarmichael(threshold) + 1


def runTests():
    assert carmichaelThreshold(6) == 241
    assert carmichaelThreshold(100) == 20_174_525_281


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = carmichaelThreshold(20_000_000) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
