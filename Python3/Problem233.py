import math
import time


LIMIT = 10 ** 11
TARGET_PRODUCT = 105
EXPONENT_PATTERNS = (
    (52,),
    (17, 1),
    (10, 2),
    (7, 3),
    (3, 2, 1),
)


def primesOneModFour(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(5, limit + 1, 4) if sieve[number]], sieve


def latticePointCount(number):
    remaining = number
    product = 1
    factor = 5

    while factor * factor <= remaining:
        exponent = 0
        while remaining % factor == 0:
            remaining //= factor
            exponent += 1

        if factor % 4 == 1 and exponent:
            product *= 2 * exponent + 1

        factor += 2

    if remaining > 1 and remaining % 4 == 1:
        product *= 3

    return 4 * product


def validPrimePowerBases(limit):
    max_prime = limit // (5 ** 3 * 13 ** 2)
    primes, _ = primesOneModFour(max_prime)
    bases = set()

    def build(pattern, used, product):
        if not pattern:
            bases.add(product)
            return

        exponent = pattern[0]
        for prime in primes:
            if prime in used:
                continue

            prime_power = prime ** exponent
            if product * prime_power > limit:
                break

            build(pattern[1:], used | {prime}, product * prime_power)

    for pattern in EXPONENT_PATTERNS:
        build(pattern, set(), 1)

    return sorted(bases)


def multiplierPrefix(maximum):
    _, prime_sieve = primesOneModFour(maximum)
    allowed = bytearray(b"\x01") * (maximum + 1)

    for prime in range(5, maximum + 1, 4):
        if prime_sieve[prime]:
            allowed[prime : maximum + 1 : prime] = b"\x00" * (
                (maximum - prime) // prime + 1
            )

    prefix = [0] * (maximum + 1)
    for number in range(1, maximum + 1):
        prefix[number] = prefix[number - 1] + (number if allowed[number] else 0)

    return prefix


def latticePointSum(limit):
    bases = validPrimePowerBases(limit)
    max_multiplier = max(limit // base for base in bases)
    prefix = multiplierPrefix(max_multiplier)

    return sum(base * prefix[limit // base] for base in bases)


def runTests():
    assert latticePointCount(10000) == 36


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = latticePointSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
