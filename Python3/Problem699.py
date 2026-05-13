import math
import random
import sys
import time


def isProbablePrime(n):
    if n < 2:
        return False

    smallPrimes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in smallPrimes:
        if n % prime == 0:
            return n == prime

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue

        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True


def pollardRho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = random.randrange(1, n)
        x = random.randrange(0, n)
        y = x
        divisor = 1

        while divisor == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = math.gcd(abs(x - y), n)

        if divisor != n:
            return divisor


def factorize(n, factors):
    if n == 1:
        return

    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % prime == 0:
            exponent = 0
            while n % prime == 0:
                n //= prime
                exponent += 1
            factors[prime] = factors.get(prime, 0) + exponent
            if n == 1:
                return
            break

    if n == 1:
        return
    if isProbablePrime(n):
        factors[n] = factors.get(n, 0) + 1
        return

    divisor = pollardRho(n)
    factorize(divisor, factors)
    factorize(n // divisor, factors)


def primeFactors(n):
    factors = {}
    factorize(n, factors)
    return factors


def divisorSum(number):
    remaining = number
    factors = primeFactors(number)
    total = 1

    for prime, exponent in factors.items():
        total *= (pow(prime, exponent + 1) - 1) // (prime - 1)
        remaining //= prime ** exponent

    assert remaining == 1
    return total


def powerOfThreeExponent(n):
    if n <= 0:
        return -1

    exponent = 0
    while n % 3 == 0:
        n //= 3
        exponent += 1

    if n == 1:
        return exponent
    return -1


def sigmaPrimePower(prime, exponent):
    return (pow(prime, exponent + 1) - 1) // (prime - 1)


def seedStates(limit):
    powers2 = [1]
    while powers2[-1] * 2 <= limit:
        powers2.append(powers2[-1] * 2)

    powers3 = [1]
    while powers3[-1] * 3 <= limit:
        powers3.append(powers3[-1] * 3)

    powers5 = [1]
    while powers5[-1] * 5 <= limit:
        powers5.append(powers5[-1] * 5)

    states = []
    for exponent2, power2 in enumerate(powers2):
        sigma2 = 2 * power2 - 1 if exponent2 else 1

        for exponent3 in range(1, len(powers3)):
            power3 = powers3[exponent3]
            if power2 * power3 > limit:
                break

            sigma3 = (3 * power3 - 1) // 2
            for exponent5, power5 in enumerate(powers5):
                n = power2 * power3 * power5
                if n > limit:
                    break

                sigma5 = (5 * power5 - 1) // 4 if exponent5 else 1
                sigma = sigma2 * sigma3 * sigma5

                common = math.gcd(n, sigma)
                numerator = sigma // common
                denominator = n // common

                if denominator != 1 and denominator % 3 == 0:
                    states.append((n, numerator, denominator))

    return states


def triffleSum(limit):
    random.seed(0)
    sys.setrecursionlimit(2_000_000)

    factorCache = {}

    def cachedFactors(number):
        if number not in factorCache:
            factorCache[number] = primeFactors(number)
        return factorCache[number]

    total = 0
    visited = set()

    def search(n, numerator, denominator):
        nonlocal total

        if n in visited:
            return
        visited.add(n)

        if powerOfThreeExponent(denominator) > 0:
            total += n

        if denominator == 1 or denominator % 3 != 0 or numerator == 1:
            return

        for prime, maxExponent in cachedFactors(numerator).items():
            if prime <= 5 or n % prime == 0:
                continue

            primePower = 1
            for exponent in range(1, maxExponent + 1):
                primePower *= prime
                if n > limit // primePower:
                    break

                newNumerator = (numerator // primePower) * sigmaPrimePower(prime, exponent)
                newDenominator = denominator
                common = math.gcd(newNumerator, newDenominator)
                search(n * primePower, newNumerator // common, newDenominator // common)

    for n, numerator, denominator in seedStates(limit):
        search(n, numerator, denominator)

    return total


def runTests():
    assert divisorSum(10) == 18
    assert triffleSum(100) == 270
    assert triffleSum(10 ** 6) == 26_089_287


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triffleSum(10 ** 14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
