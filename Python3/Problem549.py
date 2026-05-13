from math import isqrt
import time


LIMIT = 10 ** 8
SEGMENT_SIZE = 500_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"

    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )

    return [number for number in range(limit + 1) if sieve[number]]


def primePowerKempner(prime, exponent):
    count = 0
    value = 0

    while count < exponent:
        value += prime
        term = value
        while term % prime == 0:
            count += 1
            term //= prime

    return value


def primePowerKempnerValues(limit):
    values = {}

    for prime in primeSieve(isqrt(limit)):
        power = prime
        exponent = 1

        while power <= limit:
            values[power] = prime if exponent == 1 else primePowerKempner(prime, exponent)
            exponent += 1
            power *= prime

    return values


def leastFactorialDivisibleBy(n):
    best = 0
    remaining = n
    factor = 2

    while factor * factor <= remaining:
        if remaining % factor == 0:
            power = 1
            exponent = 0
            while remaining % factor == 0:
                remaining //= factor
                power *= factor
                exponent += 1
            best = max(best, primePowerKempner(factor, exponent))
        factor += 1 if factor == 2 else 2

    if remaining > 1:
        best = max(best, remaining)

    return best


def leastFactorialDivisibilitySum(limit, segmentSize=SEGMENT_SIZE):
    primes = primeSieve(isqrt(limit))
    primePowerValues = primePowerKempnerValues(limit)
    total = 0

    for start in range(2, limit + 1, segmentSize):
        end = min(limit, start + segmentSize - 1)
        residuals = list(range(start, end + 1))
        bestValues = [0] * len(residuals)

        for prime in primes:
            if prime * prime > end:
                break

            first = ((start + prime - 1) // prime) * prime
            for multiple in range(first, end + 1, prime):
                index = multiple - start
                residual = residuals[index]
                power = 1

                while residual % prime == 0:
                    residual //= prime
                    power *= prime

                residuals[index] = residual
                value = primePowerValues[power]
                if value > bestValues[index]:
                    bestValues[index] = value

        for index, residual in enumerate(residuals):
            best = bestValues[index]
            total += residual if residual > best else best

    return total


def runTests():
    assert leastFactorialDivisibleBy(10) == 5
    assert leastFactorialDivisibleBy(25) == 10
    assert leastFactorialDivisibilitySum(100) == 2_012


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastFactorialDivisibilitySum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
