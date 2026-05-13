import math
import time


def integerRoot(limit, exponent):
    low = 1
    high = 2
    while high ** exponent <= limit:
        high *= 2

    while high - low > 1:
        middle = (low + high) // 2
        if middle ** exponent <= limit:
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


def maximumExponent(limit):
    exponent = 0
    value = 1
    while value * 2 <= limit:
        value *= 2
        exponent += 1
    return exponent


def allPerfectPowers(limit):
    powers = set()
    for exponent in range(2, maximumExponent(limit) + 1):
        root = integerRoot(limit, exponent)
        for base in range(2, root + 1):
            powers.add(base ** exponent)
    return powers


def primePrimePowers(limit):
    powers = set()
    primeExponents = primeSieve(maximumExponent(limit))
    primeBases = primeSieve(math.isqrt(limit))

    for exponent in primeExponents:
        root = integerRoot(limit, exponent)
        for base in primeBases:
            if base > root:
                break
            powers.add(base ** exponent)

    return powers


def creativeNumbers(limit):
    numbers = allPerfectPowers(limit) - primePrimePowers(limit)
    if limit >= 16:
        numbers.discard(16)
    return numbers


def creativeNumberSum(limit):
    return sum(creativeNumbers(limit))


def canReachNineFromEight():
    start = 8
    base = 2
    exponent = 3
    return base ** exponent == start and exponent ** base == 9


def runTests():
    assert canReachNineFromEight()
    assert allPerfectPowers(10) == {4, 8, 9}
    assert primePrimePowers(10) == {4, 8, 9}
    assert creativeNumbers(100) == {36, 64, 81, 100}


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = creativeNumberSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
