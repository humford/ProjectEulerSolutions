from functools import lru_cache
import time


MOBIUS_LIMIT = 5_000_000


def mobiusPrefix(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    composite = bytearray(limit + 1)

    for number in range(2, limit + 1):
        if not composite[number]:
            primes.append(number)
            mu[number] = -1

        for prime in primes:
            value = number * prime
            if value > limit:
                break

            composite[value] = 1
            if number % prime == 0:
                mu[value] = 0
                break

            mu[value] = -mu[number]

    prefix = [0] * (limit + 1)
    running = 0
    for number in range(1, limit + 1):
        running += mu[number]
        prefix[number] = running

    return prefix


MOBIUS_PREFIX = mobiusPrefix(MOBIUS_LIMIT)


@lru_cache(maxsize=None)
def mertens(n):
    if n <= MOBIUS_LIMIT:
        return MOBIUS_PREFIX[n]

    total = 1
    start = 2

    while start <= n:
        quotient = n // start
        end = n // quotient
        total -= (end - start + 1) * mertens(quotient)
        start = end + 1

    return total


@lru_cache(maxsize=None)
def oddMertens(n):
    total = 0

    while n:
        total += mertens(n)
        n //= 2

    return total


def oddIntegerSum(limit):
    oddCount = (limit + 1) // 2
    return oddCount * oddCount


def oddTotientSum(limit):
    total = 0
    start = 1

    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        total += (oddMertens(end) - oddMertens(start - 1)) * oddIntegerSum(quotient)
        start = end + 1

    return total


def totientPowerSum(limit):
    return oddTotientSum(limit)


def runTests():
    assert totientPowerSum(100) == 2_007


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totientPowerSum(5 * 10**8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
