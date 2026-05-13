from math import isqrt
import time


MODULUS = 1_000_000_007
TARGET = 10**8


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"

    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )

    return sieve


def isRelevantPrime(prime):
    return prime == 2 or prime % 8 in (5, 7)


def signChangeDeltas(limit):
    # The equiproduct partition is the Thue-Morse sign on irreducible
    # exponents in Z[sqrt(-2)].  For rational factorials, split primes cancel
    # in conjugate pairs; only 2 and inert primes p = 5, 7 mod 8 remain.
    sieve = primeSieve(limit)
    root = isqrt(limit)
    deltas = bytearray(limit + 1)

    for prime in range(2, limit + 1):
        if not sieve[prime] or not isRelevantPrime(prime):
            continue

        exponent = 0
        currentParity = 0

        if prime == 2:
            multipleIndex = 1
            for multiple in range(prime, limit + 1, prime):
                exponent += (multipleIndex & -multipleIndex).bit_length()
                nextParity = exponent.bit_count() & 1
                if currentParity ^ nextParity:
                    deltas[multiple] ^= 1
                currentParity = nextParity
                multipleIndex += 1
        elif prime > root:
            multipleIndex = 1
            for multiple in range(prime, limit + 1, prime):
                nextParity = multipleIndex.bit_count() & 1
                if currentParity ^ nextParity:
                    deltas[multiple] ^= 1
                currentParity = nextParity
                multipleIndex += 1
        else:
            multipleIndex = 1
            for multiple in range(prime, limit + 1, prime):
                quotient = multipleIndex
                increment = 1

                while quotient % prime == 0:
                    quotient //= prime
                    increment += 1

                exponent += increment
                nextParity = exponent.bit_count() & 1
                if currentParity ^ nextParity:
                    deltas[multiple] ^= 1
                currentParity = nextParity
                multipleIndex += 1

    return deltas


def G(limit):
    deltas = signChangeDeltas(limit)
    parity = 0
    factorial = 1
    total = 0

    for n in range(1, limit + 1):
        parity ^= deltas[n]
        factorial = factorial * n % MODULUS

        if parity == 0:
            total = (total + factorial) % MODULUS

    return total


def solve():
    return G(TARGET)


def runTests():
    assert G(4) == 25
    assert G(7) == 745
    assert G(100) == 709_772_949


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
