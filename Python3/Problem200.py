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


def isPrime(number):
    if number < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if number == prime:
            return True
        if number % prime == 0:
            return False

    d = number - 1
    shifts = 0
    while d % 2 == 0:
        d //= 2
        shifts += 1

    for base in small_primes:
        if base >= number:
            continue

        value = pow(base, d, number)
        if value == 1 or value == number - 1:
            continue

        for _ in range(shifts - 1):
            value = pow(value, 2, number)
            if value == number - 1:
                break
        else:
            return False

    return True


def isPrimeProof(number):
    digits = list(str(number))

    for position, original in enumerate(digits):
        for replacement in "0123456789":
            if replacement == original:
                continue
            if position == 0 and replacement == "0":
                continue

            changed = digits[:]
            changed[position] = replacement
            if isPrime(int("".join(changed))):
                return False

    return True


def squbesBelow(limit):
    prime_limit = math.isqrt(limit // 8) + 1
    primes = primesUpTo(prime_limit)
    values = []

    for q in primes:
        q_cubed = q * q * q
        if 4 * q_cubed > limit:
            break

        for p in primes:
            if p == q:
                continue

            value = p * p * q_cubed
            if value > limit:
                break
            values.append(value)

    return values


def primeProofSqube(target):
    limit = 10 ** 12

    while True:
        candidates = sorted(
            value
            for value in squbesBelow(limit)
            if "200" in str(value) and isPrimeProof(value)
        )

        if len(candidates) >= target:
            return candidates[target - 1]

        limit *= 2


def runTests():
    assert isPrimeProof(200)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeProofSqube(200)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
