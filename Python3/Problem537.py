from math import isqrt, log
import time


MODULUS = 1_004_535_809
PRIMITIVE_ROOT = 3


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * ((limit - start) // p + 1)
    return [p for p in range(limit + 1) if sieve[p]]


def firstPrimes(count):
    if count < 6:
        limit = 15
    else:
        limit = int(count * (log(count) + log(log(count)))) + 20

    while True:
        primes = primeSieve(limit)
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def ntt(values, invert=False):
    length = len(values)
    swapIndex = 0

    for index in range(1, length):
        bit = length >> 1
        while swapIndex & bit:
            swapIndex ^= bit
            bit >>= 1
        swapIndex ^= bit

        if index < swapIndex:
            values[index], values[swapIndex] = values[swapIndex], values[index]

    blockLength = 2
    while blockLength <= length:
        rootStep = pow(PRIMITIVE_ROOT, (MODULUS - 1) // blockLength, MODULUS)
        if invert:
            rootStep = pow(rootStep, MODULUS - 2, MODULUS)

        halfLength = blockLength // 2
        for start in range(0, length, blockLength):
            factor = 1
            for offset in range(start, start + halfLength):
                left = values[offset]
                right = values[offset + halfLength] * factor % MODULUS
                values[offset] = (left + right) % MODULUS
                values[offset + halfLength] = (left - right) % MODULUS
                factor = factor * rootStep % MODULUS

        blockLength *= 2

    if invert:
        inverseLength = pow(length, MODULUS - 2, MODULUS)
        for index in range(length):
            values[index] = values[index] * inverseLength % MODULUS


def multiplyPolynomials(left, right, degree):
    resultLength = min(len(left) + len(right) - 1, degree + 1)
    transformLength = 1
    while transformLength < len(left) + len(right) - 1:
        transformLength *= 2

    leftValues = left + [0] * (transformLength - len(left))
    rightValues = right + [0] * (transformLength - len(right))

    ntt(leftValues)
    ntt(rightValues)
    for index in range(transformLength):
        leftValues[index] = leftValues[index] * rightValues[index] % MODULUS
    ntt(leftValues, True)

    return leftValues[:resultLength]


def tupleCount(n, k):
    primes = firstPrimes(n + 1)
    base = [1] + [
        (primes[index] - primes[index - 1]) % MODULUS
        for index in range(1, n + 1)
    ]
    result = [1]
    exponent = k

    while exponent:
        if exponent & 1:
            result = multiplyPolynomials(result, base, n)

        exponent //= 2
        if exponent:
            base = multiplyPolynomials(base, base, n)

    return result[n] if n < len(result) else 0


def runTests():
    assert tupleCount(3, 3) == 19
    assert tupleCount(10, 10) == 869_985
    assert tupleCount(1_000, 1_000) == 578_270_566


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = tupleCount(20_000, 20_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
