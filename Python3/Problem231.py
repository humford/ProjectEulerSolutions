import math
import time


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(limit + 1) if sieve[number]]


def exponentInFactorial(number, prime):
    total = 0
    while number:
        number //= prime
        total += number
    return total


def primeFactorSumBinomial(n, k):
    total = 0
    for prime in primesUpTo(n):
        exponent = (
            exponentInFactorial(n, prime)
            - exponentInFactorial(k, prime)
            - exponentInFactorial(n - k, prime)
        )
        total += prime * exponent

    return total


def runTests():
    assert primeFactorSumBinomial(10, 3) == 14


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeFactorSumBinomial(20000000, 15000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
