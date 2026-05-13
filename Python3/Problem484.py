import math
import time


def arithmeticDerivative(n):
    if n < 2:
        return 0
    original = n
    factor = 2
    total = 0
    while factor * factor <= n:
        if n % factor == 0:
            exponent = 0
            while n % factor == 0:
                n //= factor
                exponent += 1
            total += exponent * original // factor
        factor += 1 if factor == 2 else 2
    if n > 1:
        total += original // n
    return total


def primeSieve(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit // 2 + 1)
    sieve[0] = 0

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number // 2]:
            start = number * number // 2
            sieve[start::number] = b"\x00" * ((len(sieve) - start - 1) // number + 1)

    primes = [2]
    primes.extend(2 * index + 1 for index in range(1, len(sieve)) if sieve[index])
    return primes


def bruteGcdDerivativeSum(limit):
    return sum(math.gcd(n, arithmeticDerivative(n)) for n in range(2, limit + 1))


def gcdDerivativeSum(limit):
    primes = primeSieve(math.isqrt(limit))
    primeCount = len(primes)

    def powerfulContribution(startIndex, remaining):
        total = 0

        for primeIndex in range(startIndex, primeCount):
            prime = primes[primeIndex]
            primeSquared = prime * prime
            quotient = remaining // primeSquared
            if quotient == 0:
                break

            exponentModPrime = 1
            previousGcdPrimePower = 1

            while quotient:
                oldGcdPrimePower = previousGcdPrimePower
                exponentModPrime += 1

                if exponentModPrime != 1:
                    if exponentModPrime == prime:
                        previousGcdPrimePower *= primeSquared
                        exponentModPrime = 0
                    else:
                        previousGcdPrimePower *= prime

                    mobiusDelta = previousGcdPrimePower - oldGcdPrimePower
                    total += mobiusDelta * quotient

                    if quotient > primeSquared:
                        total += mobiusDelta * powerfulContribution(primeIndex + 1, quotient)

                quotient //= prime

        return total

    return limit - 1 + powerfulContribution(0, limit)


def runTests():
    assert arithmeticDerivative(20) == 24
    assert math.gcd(20, arithmeticDerivative(20)) == 4
    assert gcdDerivativeSum(10) == bruteGcdDerivativeSum(10)
    assert gcdDerivativeSum(100) == bruteGcdDerivativeSum(100)
    assert gcdDerivativeSum(1000) == bruteGcdDerivativeSum(1000)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gcdDerivativeSum(5 * 10 ** 15)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
