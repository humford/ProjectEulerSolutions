import math
import time


START = 10**14
COUNT = 100000
MODULUS = 1234567891011
SEGMENT_ODDS = 5_000_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    if limit >= 4:
        sieve[4 : limit + 1 : 2] = b"\x00" * ((limit - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            step = 2 * number
            start = number * number
            sieve[start : limit + 1 : step] = b"\x00" * (
                (limit - start) // step + 1
            )

    return [2] + [number for number in range(3, limit + 1, 2) if sieve[number]]


def primesAfter(start, count):
    base_limit = math.isqrt(start + 20_000_000) + 100
    base_primes = primeSieve(base_limit)
    primes = []
    low = start + 1

    if low % 2 == 0:
        low += 1

    while len(primes) < count:
        high = low + 2 * SEGMENT_ODDS
        size = (high - low) // 2
        segment = bytearray(b"\x01") * size

        if base_primes[-1] * base_primes[-1] < high:
            base_primes = primeSieve(math.isqrt(high) + 100)

        for prime in base_primes[1:]:
            if prime * prime >= high:
                break

            first = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if first % 2 == 0:
                first += prime

            index = (first - low) // 2
            if index < size:
                segment[index::prime] = b"\x00" * ((size - 1 - index) // prime + 1)

        for index, is_prime in enumerate(segment):
            if is_prime:
                primes.append(low + 2 * index)
                if len(primes) == count:
                    return primes

        low = high | 1

    return primes


def fibonacciMod(index):
    if index == 0:
        return 0, 1

    a, b = fibonacciMod(index // 2)
    c = a * ((2 * b - a) % MODULUS) % MODULUS
    d = (a * a + b * b) % MODULUS

    if index % 2:
        return d, (c + d) % MODULUS

    return c, d


def primonacciSum(start, count):
    return sum(fibonacciMod(prime)[0] for prime in primesAfter(start, count)) % MODULUS


def runTests():
    assert primesAfter(100, 5) == [101, 103, 107, 109, 113]
    assert fibonacciMod(10)[0] == 55


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primonacciSum(START, COUNT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
