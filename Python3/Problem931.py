from array import array
from math import isqrt
import time


MODULUS = 715_827_883
TARGET_N = 10**12
INVERSE_TWO = pow(2, -1, MODULUS)


def triangular(n):
    return (n % MODULUS) * ((n + 1) % MODULUS) * INVERSE_TWO % MODULUS


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, isqrt(limit) + 1):
        if isPrime[n]:
            isPrime[n * n:limit + 1:n] = b"\x00" * (((limit - n * n) // n) + 1)

    return [n for n in range(2, limit + 1) if isPrime[n]]


def primeCountAndSumTables(limit):
    root = isqrt(limit)
    values = []
    n = 1

    while n <= limit:
        value = limit // n
        values.append(value)
        n = limit // value + 1

    smallIndex = array("i", [-1]) * (root + 1)
    largeIndex = array("i", [-1]) * (root + 1)

    for index, value in enumerate(values):
        if value <= root:
            smallIndex[value] = index
        else:
            largeIndex[limit // value] = index

    primeCounts = [value - 1 for value in values]
    primeSums = [(triangular(value) - 1) % MODULUS for value in values]

    def tableIndex(value):
        if value <= root:
            return smallIndex[value]
        return largeIndex[limit // value]

    for p in range(2, root + 1):
        pIndex = tableIndex(p)
        previousIndex = tableIndex(p - 1)

        if primeCounts[pIndex] == primeCounts[previousIndex]:
            continue

        previousCount = primeCounts[previousIndex]
        previousSum = primeSums[previousIndex]
        pSquared = p * p

        for index, value in enumerate(values):
            if value < pSquared:
                break

            quotientIndex = tableIndex(value // p)
            primeCounts[index] -= primeCounts[quotientIndex] - previousCount
            primeSums[index] = (
                primeSums[index]
                - p * (primeSums[quotientIndex] - previousSum)
            ) % MODULUS

    return values, primeCounts, primeSums, tableIndex


def totientGraphWeight(n):
    total = 0
    remaining = n
    factor = 2

    while factor * factor <= remaining:
        if remaining % factor == 0:
            primePower = 1
            while remaining % factor == 0:
                remaining //= factor
                primePower *= factor

            phi = primePower // factor * (factor - 1)
            total += n // primePower * (phi - 1)

        factor += 1 if factor == 2 else 2

    if remaining > 1:
        total += n // remaining * (remaining - 2)

    return total


def directT(limit):
    return sum(totientGraphWeight(n) for n in range(1, limit + 1))


def coprimeWeightedSum(limit, prime):
    return (triangular(limit) - prime * triangular(limit // prime)) % MODULUS


def T(limit):
    root = isqrt(limit)
    primes = primeSieve(root)
    _, primeCounts, primeSums, tableIndex = primeCountAndSumTables(limit)

    answer = 0

    # First powers p <= sqrt(N) are handled directly because the correction
    # excluding multiples of p in m is nonzero there.
    for prime in primes:
        x = limit // prime
        answer = (
            answer
            + (prime - 2) * coprimeWeightedSum(x, prime)
        ) % MODULUS

    # For p > sqrt(N), floor(N / p) < sqrt(N), and m is automatically coprime
    # to p.  Group these primes by the common value of floor(N / p).
    for quotient in range(1, root):
        low = limit // (quotient + 1) + 1
        high = limit // quotient

        if high <= root:
            continue
        if low <= root:
            low = root + 1

        highIndex = tableIndex(high)
        lowIndex = tableIndex(low - 1)
        count = (primeCounts[highIndex] - primeCounts[lowIndex]) % MODULUS
        primeSum = (primeSums[highIndex] - primeSums[lowIndex]) % MODULUS
        answer = (
            answer
            + triangular(quotient) * (primeSum - 2 * count)
        ) % MODULUS

    # Higher prime powers all have p <= sqrt(N).
    for prime in primes:
        primePower = prime * prime
        previousPower = prime

        while primePower <= limit:
            phi = previousPower * (prime - 1)
            coefficient = phi - 1
            x = limit // primePower
            answer = (
                answer
                + coefficient * coprimeWeightedSum(x, prime)
            ) % MODULUS

            previousPower = primePower
            primePower *= prime

    return answer


def solve():
    return T(TARGET_N)


def runTests():
    assert totientGraphWeight(45) == 52
    assert directT(10) == 26
    assert directT(100) == 5282


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
