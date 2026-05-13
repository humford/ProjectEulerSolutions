import math
import time


COUNT = 4


SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            sieve[number * number : limit + 1 : number] = b"\x00" * (
                (limit - number * number) // number + 1
            )

    return [number for number in range(limit + 1) if sieve[number]]


FACTOR_PRIMES = primeSieve(40000)


def isPrime(number):
    if number < 2:
        return False

    for prime in SMALL_PRIMES:
        if number % prime == 0:
            return number == prime

    odd_part = number - 1
    shift = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        shift += 1

    for base in (2, 3, 5, 7, 11):
        if base >= number:
            continue

        value = pow(base, odd_part, number)
        if value == 1 or value == number - 1:
            continue

        for _ in range(shift - 1):
            value = (value * value) % number
            if value == number - 1:
                break
        else:
            return False

    return True


def factorization(number):
    result = []
    remaining = number

    for prime in FACTOR_PRIMES:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            result.append((prime, exponent))

    if remaining > 1:
        result.append((remaining, 1))

    return result


def isPractical(number):
    factors = factorization(number)
    if not factors or factors[0][0] != 2:
        return number == 1

    reachable_sum = 1
    for prime, exponent in factors:
        if prime > reachable_sum + 1:
            return False
        reachable_sum *= (prime ** (exponent + 1) - 1) // (prime - 1)

    return True


def isEngineersParadise(number):
    if not (
        isPrime(number - 9)
        and isPrime(number - 3)
        and isPrime(number + 3)
        and isPrime(number + 9)
    ):
        return False

    for offset in (-7, -5, -1, 1, 5, 7):
        if isPrime(number + offset):
            return False

    return all(isPractical(number + offset) for offset in (-8, -4, 0, 4, 8))


def engineersParadises(count):
    result = []
    multiplier = 0

    while len(result) < count:
        for candidate in (840 * multiplier + 20, 840 * multiplier + 820):
            if isEngineersParadise(candidate):
                result.append(candidate)
                if len(result) == count:
                    break
        multiplier += 1

    return result


def engineersParadiseSum(count):
    return sum(engineersParadises(count))


def runTests():
    assert isPractical(6)
    assert not isPractical(10)
    assert engineersParadises(1) == [219869980]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = engineersParadiseSum(COUNT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
