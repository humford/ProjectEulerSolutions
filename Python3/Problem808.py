import math
import time


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for n in range(2, math.isqrt(limit) + 1):
        if sieve[n]:
            start = n * n
            sieve[start: limit + 1: n] = b"\x00" * ((limit - start) // n + 1)

    return sieve


def isPrime(n):
    if n < 2:
        return False

    smallPrimes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in smallPrimes:
        if n % prime == 0:
            return n == prime

    oddPart = n - 1
    shifts = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        shifts += 1

    for witness in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if witness % n == 0:
            continue

        x = pow(witness, oddPart, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(shifts - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True


def reverseNumber(n):
    return int(str(n)[::-1])


def isReversiblePrimeSquare(square, primeFlags=None):
    reversedSquare = reverseNumber(square)
    if reversedSquare == square:
        return False

    root = math.isqrt(reversedSquare)
    if root * root != reversedSquare:
        return False

    if primeFlags is not None and root < len(primeFlags):
        return bool(primeFlags[root])

    return isPrime(root)


def firstReversiblePrimeSquares(count, initialLimit=10_000_000):
    limit = initialLimit

    while True:
        primeFlags = primeSieve(limit)
        values = []

        for prime in range(2, limit + 1):
            if not primeFlags[prime]:
                continue

            square = prime * prime
            if isReversiblePrimeSquare(square, primeFlags):
                values.append(square)
                if len(values) == count:
                    return values

        limit *= 2


def reversiblePrimeSquareSum(count):
    return sum(firstReversiblePrimeSquares(count))


def runTests():
    values = firstReversiblePrimeSquares(2, 100)
    assert values == [169, 961]
    assert not isReversiblePrimeSquare(121, primeSieve(100))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reversiblePrimeSquareSum(50)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
