import math
import time


def primesUpTo(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)

    return [number for number in range(2, limit + 1) if sieve[number]]


def primesInRange(start, length):
    stop = start + length
    if stop <= 2:
        return

    segment = bytearray(b"\x01") * length
    for offset in range(max(0, 2 - start)):
        segment[offset] = 0

    for prime in primesUpTo(math.isqrt(stop - 1)):
        firstMultiple = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if firstMultiple < stop:
            segment[firstMultiple - start : length : prime] = b"\x00" * (
                ((stop - 1 - firstMultiple) // prime) + 1
            )

    for offset, isPrime in enumerate(segment):
        if isPrime:
            yield start + offset


def bruteDModPrime(prime, k):
    values = [0] + [pow(number, -1, prime) for number in range(1, prime)]
    for _ in range(k):
        runningTotal = 0
        nextValues = [0] * prime
        for number in range(1, prime):
            runningTotal = (runningTotal + values[number]) % prime
            nextValues[number] = runningTotal
        values = nextValues

    return values[prime - 1]


def dModPrime(prime, k):
    if k == 0:
        return prime - 1
    if k == 1:
        return 0
    if prime <= k - 1:
        return bruteDModPrime(prime, k)

    # Repeated prefix sums give
    # d(p, n, k) = sum_{i=1..n} i^(-1) * C(n + k - i - 1, k - 1).
    # Setting n = p - 1 and reducing the binomial expression modulo p makes
    # the sum telescope to 1 / (k - 1) modulo p.
    return pow(k - 1, -1, prime)


def dissonantSum(start, length, k):
    return sum(dModPrime(prime, k) for prime in primesInRange(start, length))


def runTests():
    assert dModPrime(11, 3) == bruteDModPrime(11, 3)
    assert dModPrime(101, 10) == bruteDModPrime(101, 10)
    assert dissonantSum(101, 1, 10) == 45
    assert dissonantSum(10 ** 3, 10 ** 2, 10 ** 2) == 8_334
    assert dissonantSum(10 ** 6, 10 ** 3, 10 ** 3) == 38_162_302


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = dissonantSum(10 ** 9, 10 ** 5, 10 ** 5)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
