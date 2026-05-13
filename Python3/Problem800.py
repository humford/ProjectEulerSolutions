import math
import time


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, math.isqrt(limit) + 1):
        if isPrime[n]:
            isPrime[n * n:limit + 1:n] = b"\x00" * (((limit - n * n) // n) + 1)

    return [n for n in range(limit + 1) if isPrime[n]]


def C(base, exponent):
    logLimit = exponent * math.log(base)
    primeLimit = int(logLimit / math.log(2)) + 100
    primes = primeSieve(primeLimit)
    logs = [math.log(prime) for prime in primes]

    total = 0
    right = len(primes) - 1
    tolerance = 1e-12 * max(1.0, logLimit)

    for left, p in enumerate(primes):
        if right <= left:
            break

        logP = logs[left]
        while right > left and primes[right] * logP + p * logs[right] > logLimit + tolerance:
            right -= 1

        if right <= left:
            break
        total += right - left

    return total


def runTests():
    assert C(800, 1) == 2
    assert C(800, 800) == 10_790


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = C(800_800, 800_800)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
