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

    return [number for number in range(3, limit + 1, 2) if sieve[number]]


def squareRootInverseTwo(prime):
    if prime % 8 == 7:
        return (pow(2, (prime + 1) // 4, prime) * ((prime + 1) // 2)) % prime

    n = (prime + 1) // 2
    q = prime - 1
    shifts = 0
    while q % 2 == 0:
        shifts += 1
        q //= 2

    z = 2
    while pow(z, (prime - 1) // 2, prime) != prime - 1:
        z += 1

    m = shifts
    c = pow(z, q, prime)
    t = pow(n, q, prime)
    root = pow(n, (q + 1) // 2, prime)

    while t != 1:
        i = 1
        t2 = (t * t) % prime
        while t2 != 1:
            t2 = (t2 * t2) % prime
            i += 1

        b = pow(c, 1 << (m - i - 1), prime)
        m = i
        c = (b * b) % prime
        t = (t * c) % prime
        root = (root * b) % prime

    return root


def quadraticPrimeCount(limit):
    prime_limit = math.isqrt(2 * limit * limit - 1)
    candidates = bytearray(b"\x01") * (limit + 1)
    candidates[0] = 0
    candidates[1] = 0

    for prime in primesUpTo(prime_limit):
        if prime % 8 not in (1, 7):
            continue

        root = squareRootInverseTwo(prime)
        for solution in (root, prime - root):
            start = solution
            if 2 * solution * solution - 1 == prime:
                start += prime

            if start <= limit:
                candidates[start : limit + 1 : prime] = b"\x00" * (
                    (limit - start) // prime + 1
                )

    return candidates.count(1)


def runTests():
    assert quadraticPrimeCount(10) == 7


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = quadraticPrimeCount(50000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
