import math
import time


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    if limit > 0:
        sieve[0] = 0
    if limit > 1:
        sieve[1] = 0

    for prime in range(2, math.isqrt(limit - 1) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit:prime] = b"\x00" * (((limit - 1 - start) // prime) + 1)

    return sieve


def coprimeResidues(limit):
    return [number for number in range(1, limit) if math.gcd(number, limit) == 1]


def primeTripleSum(limit):
    isPrime = primeSieve(limit)
    total = 0

    # If a+1, b+1, c+1 are geometric, write them as
    # d*r^2, d*r*s, d*s^2 with gcd(r, s) = 1 and r < s.
    for s in range(2, math.isqrt(limit) + 1):
        square = s * s
        maxMultiplier = limit // square
        residues = coprimeResidues(s)

        for multiplier in range(1, maxMultiplier + 1):
            c = multiplier * square - 1
            if not isPrime[c]:
                continue

            middleFactor = multiplier * s
            for r in residues:
                a = multiplier * r * r - 1
                b = middleFactor * r - 1
                if isPrime[a] and isPrime[b]:
                    total += a + b + c

    return total


def runTests():
    assert primeTripleSum(100) == 1_035


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeTripleSum(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
