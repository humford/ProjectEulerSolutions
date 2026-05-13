import time
from array import array


G = 10**6
L = 10**12
N = 10**18
MODULUS = 101**4


def smallestPrimeFactors(limit):
    spf = array("I", [0]) * (limit + 1)
    primes = []

    if limit >= 1:
        spf[1] = 1

    for number in range(2, limit + 1):
        if spf[number] == 0:
            spf[number] = number
            primes.append(number)

        leastFactor = spf[number]

        for prime in primes:
            multiple = number * prime

            if multiple > limit or prime > leastFactor:
                break

            spf[multiple] = prime

    return spf


def coprimeLcmPrefix(limit, length, modulus):
    maxExponent = 0
    value = limit

    while value > 1:
        value //= 2
        maxExponent += 1

    powers = [pow(base, length, modulus) for base in range(maxExponent + 2)]
    primePowerCounts = [0] * (maxExponent + 1)

    for exponent in range(1, maxExponent + 1):
        primePowerCounts[exponent] = (
            powers[exponent + 1] - 2 * powers[exponent] + powers[exponent - 1]
        ) % modulus

    spf = smallestPrimeFactors(limit)
    exponents = bytearray(limit + 1)
    rest = array("I", [0]) * (limit + 1)
    counts = array("I", [0]) * (limit + 1)
    rest[1] = 1
    counts[1] = 1

    for number in range(2, limit + 1):
        prime = spf[number]
        quotient = number // prime

        if spf[quotient] == prime:
            exponents[number] = exponents[quotient] + 1
            rest[number] = rest[quotient]
        else:
            exponents[number] = 1
            rest[number] = quotient

        counts[number] = (
            counts[rest[number]] * primePowerCounts[exponents[number]]
        ) % modulus

    prefix = array("I", [0]) * (limit + 1)
    running = 0

    for number in range(1, limit + 1):
        running = (running + counts[number]) % modulus
        prefix[number] = running

    return prefix


def constrainedListCount(g, l, length, modulus=MODULUS):
    if g > l:
        return 0

    limit = l // g
    prefix = coprimeLcmPrefix(limit, length, modulus)
    total = 0
    divisor = g

    while divisor <= l:
        quotient = l // divisor
        nextDivisor = l // quotient
        total = (
            total + ((nextDivisor - divisor + 1) % modulus) * prefix[quotient]
        ) % modulus
        divisor = nextDivisor + 1

    return total


def runTests():
    assert constrainedListCount(10, 100, 1) == 91
    assert constrainedListCount(10, 100, 2) == 327
    assert constrainedListCount(10, 100, 3) == 1135
    assert constrainedListCount(10, 100, 1000) == 3286053


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = constrainedListCount(G, L, N)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
