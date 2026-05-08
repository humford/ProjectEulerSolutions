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


def hammingCount(hamming_type, limit):
    primes = primesUpTo(hamming_type)

    def countFrom(index, current):
        if index == len(primes):
            return 1

        total = 0
        value = current
        while value <= limit:
            total += countFrom(index + 1, value)
            value *= primes[index]

        return total

    return countFrom(0, 1)


def runTests():
    assert hammingCount(5, 100) == 34


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hammingCount(100, 1000000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
