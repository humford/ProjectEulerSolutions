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


def factorization(number, primes):
    factors = []
    remaining = number

    for prime in primes:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            factors.append((prime, exponent))

    if remaining > 1:
        factors.append((remaining, 1))

    return factors


def divisorsFromFactors(factors):
    divisors = [1]
    for prime, exponent in factors:
        current = []
        value = 1
        for _ in range(exponent + 1):
            current.extend(divisor * value for divisor in divisors)
            value *= prime
        divisors = current

    return divisors


def alexandrianInteger(index):
    candidates = set()
    limit = 0
    batch = 10000

    while True:
        next_limit = limit + batch
        primes = primesUpTo(next_limit + 1)

        for n in range(limit + 1, next_limit + 1):
            value = n * n + 1
            root = math.isqrt(value)
            for divisor in divisorsFromFactors(factorization(value, primes)):
                if divisor <= root:
                    candidates.add(n * (n + divisor) * (n + value // divisor))

        limit = next_limit
        if len(candidates) >= index:
            ordered = sorted(candidates)
            kth = ordered[index - 1]
            if 4 * (limit + 1) ** 3 > kth:
                return kth


def runTests():
    first = [alexandrianInteger(index) for index in range(1, 7)]
    assert first == [6, 42, 120, 156, 420, 630]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = alexandrianInteger(150000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
