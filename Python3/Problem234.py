import math
import time


LIMIT = 999966663333


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


def multipleSum(multiple, low_exclusive, high_inclusive):
    first = ((low_exclusive // multiple) + 1) * multiple
    last = (high_inclusive // multiple) * multiple

    if first > last:
        return 0

    count = (last - first) // multiple + 1
    return count * (first + last) // 2


def semidivisibleSum(limit):
    primes = primesUpTo(math.isqrt(limit) + 100)
    total = 0

    for lower, upper in zip(primes, primes[1:]):
        low = lower * lower
        if low > limit:
            break

        high = min(upper * upper - 1, limit)
        total += multipleSum(lower, low, high)
        total += multipleSum(upper, low, high)
        total -= 2 * multipleSum(lower * upper, low, high)

    return total


def runTests():
    assert semidivisibleSum(15) == 30
    assert semidivisibleSum(1000) == 34825


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = semidivisibleSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
