import math
import time
from functools import lru_cache


MODULUS = 10 ** 9
TARGET_CHAINS = 252


def integerCubeRoot(number):
    low = 0
    high = 1
    while high ** 3 <= number:
        high *= 2

    while high - low > 1:
        middle = (low + high) // 2
        if middle ** 3 <= number:
            low = middle
        else:
            high = middle

    return low


def primeSieve(limit):
    if limit < 2:
        return []

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if isPrime[prime]:
            start = prime * prime
            isPrime[start : limit + 1 : prime] = b"\x00" * (
                ((limit - start) // prime) + 1
            )

    return [number for number, prime in enumerate(isPrime) if prime]


@lru_cache(maxsize=None)
def gozintaChainCount(exponents):
    totalExponent = sum(exponents)
    total = 0

    for factorCount in range(1, totalExponent + 1):
        exact = 0
        for emptyFactors in range(factorCount):
            usedFactors = factorCount - emptyFactors
            ways = 1
            for exponent in exponents:
                ways *= math.comb(exponent + usedFactors - 1, usedFactors - 1)
            exact += (-1) ** emptyFactors * math.comb(factorCount, emptyFactors) * ways
        total += exact

    return total


def signaturesWithChainCount(target):
    signatures = []
    maxExponent = target.bit_length()

    def search(maxPart, current):
        if current:
            count = gozintaChainCount(tuple(current))
            if count == target:
                signatures.append(tuple(current))
                return
            if count > target:
                return

        for exponent in range(min(maxPart, maxExponent), 0, -1):
            current.append(exponent)
            if gozintaChainCount(tuple(current)) <= target:
                search(exponent, current)
            current.pop()

    search(maxExponent, [])
    return sorted(signatures, reverse=True)


def exactGozinta252Sum(limit):
    cubeRoot = integerCubeRoot(limit)
    primes = primeSieve(cubeRoot)
    total = 0

    for index, p in enumerate(primes):
        for q in primes[index + 1 :]:
            product = p * q
            if product > cubeRoot:
                break
            total += product ** 3

    return total


def primeCubePrefixSums(limit, modulus):
    root = math.isqrt(limit)
    primes = primeSieve(root)

    values = [limit // index for index in range(1, root + 1)]
    values.extend(range(values[-1] - 1, 0, -1))
    sums = [0] * len(values)

    for index, value in enumerate(values):
        triangular = (value * (value + 1) // 2) % modulus
        sums[index] = (triangular * triangular - 1) % modulus

    def smallIndex(value):
        return len(values) - value

    for prime in primes:
        primeSquared = prime * prime
        primeCubed = pow(prime, 3, modulus)
        if primeSquared > limit:
            break

        previousPrimeCubeSum = 0 if prime == 2 else sums[smallIndex(prime - 1)]

        bigUpdateCount = min(root, limit // primeSquared)
        for index in range(bigUpdateCount):
            denominator = (index + 1) * prime
            if denominator <= root:
                reducedSum = sums[denominator - 1]
            else:
                reducedSum = sums[smallIndex(values[index] // prime)]
            sums[index] = (
                sums[index]
                - primeCubed * ((reducedSum - previousPrimeCubeSum) % modulus)
            ) % modulus

        smallUpdateCount = root - primeSquared
        for index in range(root, root + max(0, smallUpdateCount)):
            reducedSum = sums[smallIndex(values[index] // prime)]
            sums[index] = (
                sums[index]
                - primeCubed * ((reducedSum - previousPrimeCubeSum) % modulus)
            ) % modulus

    return values, sums


def gozinta252SumLastNineDigits(limit):
    signatures = signaturesWithChainCount(TARGET_CHAINS)
    if signatures != [(3, 3)]:
        raise RuntimeError("unexpected exponent signature for 252 gozinta chains")

    cubeRoot = integerCubeRoot(limit)
    root = math.isqrt(cubeRoot)
    primes = primeSieve(root)
    values, primeCubeSums = primeCubePrefixSums(cubeRoot, MODULUS)

    def smallIndex(value):
        return len(values) - value

    total = 0
    for prime in primes:
        if cubeRoot // prime <= prime:
            break
        qCubeSum = (primeCubeSums[prime - 1] - primeCubeSums[smallIndex(prime)]) % MODULUS
        total = (total + pow(prime, 3, MODULUS) * qCubeSum) % MODULUS

    return total


def runTests():
    assert integerCubeRoot(10 ** 6) == 100
    assert integerCubeRoot(10 ** 12) == 10_000
    assert gozintaChainCount((2, 1)) == 8
    assert signaturesWithChainCount(TARGET_CHAINS) == [(3, 3)]
    assert exactGozinta252Sum(10 ** 6) == 8_462_952
    assert exactGozinta252Sum(10 ** 12) == 623_291_998_881_978
    assert gozinta252SumLastNineDigits(10 ** 12) == 998_881_978


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gozinta252SumLastNineDigits(10 ** 36)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
