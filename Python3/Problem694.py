import time
from math import isqrt


TARGET = 10 ** 18


def integerCubeRoot(number):
    low = 0
    high = isqrt(number) + 1
    while low + 1 < high:
        middle = (low + high) // 2
        if middle ** 3 <= number:
            low = middle
        else:
            high = middle
    return low


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for number in range(2, isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start: limit + 1: number] = (
                b"\x00" * ((limit - start) // number + 1)
            )
    return [number for number in range(2, limit + 1) if sieve[number]]


def isCubeFull(number):
    if number == 1:
        return True
    factor = 2
    while factor * factor <= number:
        exponent = 0
        while number % factor == 0:
            number //= factor
            exponent += 1
        if exponent and exponent < 3:
            return False
        factor += 1 if factor == 2 else 2
    return number == 1


def cubeFullSummatory(limit):
    primes = primesUpTo(integerCubeRoot(limit))
    total = limit

    def generate(current, startIndex):
        subtotal = 0
        for index in range(startIndex, len(primes)):
            prime = primes[index]
            value = current * prime ** 3
            if value > limit:
                break
            while value <= limit:
                subtotal += limit // value
                subtotal += generate(value, index + 1)
                value *= prime
        return subtotal

    return total + generate(1, 0)


def bruteForceCubeFullSummatory(limit):
    return sum(limit // divisor
               for divisor in range(1, limit + 1)
               if isCubeFull(divisor))


def runTests():
    assert isCubeFull(1)
    assert isCubeFull(8)
    assert isCubeFull(16)
    assert bruteForceCubeFullSummatory(16) == 19
    assert bruteForceCubeFullSummatory(100) == 126
    assert cubeFullSummatory(16) == 19
    assert cubeFullSummatory(100) == 126
    assert cubeFullSummatory(10_000) == 13_344


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cubeFullSummatory(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
