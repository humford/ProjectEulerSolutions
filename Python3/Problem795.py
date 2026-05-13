import time
from array import array
from math import gcd


def APrimePower(prime, exponent):
    if exponent == 0:
        return 1

    if exponent % 2:
        k = exponent // 2
        return pow(prime, exponent - 1) * (2 * pow(prime, k + 1) - 1)

    k = exponent // 2
    return pow(prime, exponent - 1) * ((prime + 1) * pow(prime, k) - 1)


def smallestPrimeFactorSieve(limit):
    smallestPrimeFactor = array("I", [0]) * (limit + 1)
    primes = []

    for n in range(2, limit + 1):
        if smallestPrimeFactor[n] == 0:
            smallestPrimeFactor[n] = n
            primes.append(n)

        for prime in primes:
            value = n * prime
            if value > limit:
                break
            smallestPrimeFactor[value] = prime
            if prime == smallestPrimeFactor[n]:
                break

    return smallestPrimeFactor


def AOdd(n, smallestPrimeFactor):
    if n == 1:
        return 1

    result = 1
    while n > 1:
        prime = smallestPrimeFactor[n]
        exponent = 1
        n //= prime
        while n % prime == 0:
            n //= prime
            exponent += 1
        result *= APrimePower(prime, exponent)
    return result


def powerOfTwoCorrections(N):
    corrections = [0] * (N.bit_length() + 1)
    for exponent in range(1, len(corrections)):
        if (1 << exponent) > N:
            break
        corrections[exponent] = APrimePower(2, exponent) - (1 << exponent)
    return corrections


def g(n, smallestPrimeFactor, corrections):
    if n % 2:
        return -n

    twos = (n & -n).bit_length() - 1
    oddPart = n >> twos
    return AOdd(oddPart, smallestPrimeFactor) * corrections[twos]


def naiveG(n):
    return sum((1 if i % 2 == 0 else -1) * gcd(n, i * i) for i in range(1, n + 1))


def G(N):
    if N <= 0:
        return 0

    limit = N // 2
    smallestPrimeFactor = smallestPrimeFactorSieve(limit)
    corrections = powerOfTwoCorrections(N)

    oddCount = (N + 1) // 2
    total = -oddCount * oddCount

    for oddPart in range(1, limit + 1, 2):
        aOdd = AOdd(oddPart, smallestPrimeFactor)
        exponent = 1
        value = oddPart << 1
        while value <= N:
            total += aOdd * corrections[exponent]
            exponent += 1
            value <<= 1

    return total


def runTests():
    smallSpf = smallestPrimeFactorSieve(1234 // 2)
    corrections = powerOfTwoCorrections(1234)
    assert naiveG(4) == 6
    assert g(4, smallSpf, corrections) == 6
    assert g(1234, smallSpf, corrections) == 1_233
    assert G(1234) == 2_194_708


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = G(12_345_678)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
