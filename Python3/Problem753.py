import math
import time
from array import array


LIMIT = 6_000_000


def primeSieve(limit):
    if limit < 2:
        return bytearray(b"\x00"), []

    oddCount = limit // 2 + 1
    isOddPrime = bytearray(b"\x01") * oddCount
    isOddPrime[0] = 0

    for index in range(1, math.isqrt(limit) // 2 + 1):
        if isOddPrime[index]:
            prime = 2 * index + 1
            start = prime * prime // 2
            isOddPrime[start::prime] = b"\x00" * (((oddCount - 1 - start) // prime) + 1)

    primes = [2]
    primes.extend(2 * index + 1 for index in range(1, oddCount) if isOddPrime[index])
    if primes[-1] > limit:
        primes.pop()

    return isOddPrime, primes


def traceLookup(limit, isOddPrime):
    uByPrime = array("H", [0]) * (limit + 1)
    maxV = math.isqrt(4 * limit // 27)

    for v in range(1, maxV + 1):
        base = 27 * v * v
        maxU = math.isqrt(4 * limit - base)
        u = v % 2

        while u <= maxU:
            p = (u * u + base) // 4
            if (
                p <= limit
                and p % 3 == 1
                and p % 2 == 1
                and isOddPrime[p // 2]
                and uByPrime[p] == 0
            ):
                uByPrime[p] = u
            u += 2

    return uByPrime


def ellipticTrace(p, uByPrime):
    if p % 3 == 2:
        return 0

    u = uByPrime[p]
    if u == 0:
        raise RuntimeError("missing trace data for prime " + str(p))
    return u if u % 3 == 2 else -u


def fermatSolutionCount(p, uByPrime):
    if p == 3:
        return bruteFermatSolutionCount(p)
    if p % 3 == 2:
        return (p - 1) * (p - 2)

    trace = ellipticTrace(p, uByPrime)
    return (p - 1) * (p - trace - 8)


def bruteFermatSolutionCount(p):
    cubes = [pow(number, 3, p) for number in range(p)]
    count = 0
    for a in range(1, p):
        aCube = cubes[a]
        for b in range(1, p):
            target = (aCube + cubes[b]) % p
            for c in range(1, p):
                if cubes[c] == target:
                    count += 1
    return count


def fermatPrimeSum(limit):
    isOddPrime, primes = primeSieve(limit - 1)
    uByPrime = traceLookup(limit - 1, isOddPrime)

    total = 0
    for prime in primes:
        if prime >= limit:
            break
        total += fermatSolutionCount(prime, uByPrime)
    return total


def runTests():
    isOddPrime, _ = primeSieve(50)
    uByPrime = traceLookup(50, isOddPrime)
    assert fermatSolutionCount(5, uByPrime) == 12
    assert fermatSolutionCount(7, uByPrime) == 0
    for prime in (3, 11, 13, 17, 19, 37, 43):
        assert fermatSolutionCount(prime, uByPrime) == bruteFermatSolutionCount(prime)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fermatPrimeSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
