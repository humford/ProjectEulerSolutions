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


def semiprimeCount(limit):
    primes = primesUpTo(limit // 2)
    count = 0
    upper = len(primes) - 1

    for lower, prime in enumerate(primes):
        while upper >= lower and prime * primes[upper] >= limit:
            upper -= 1
        if upper < lower:
            break
        count += upper - lower + 1

    return count


def runTests():
    assert semiprimeCount(30) == 10


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = semiprimeCount(100000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
