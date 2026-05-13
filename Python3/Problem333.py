import math
import time


LIMIT = 1_000_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    sieve[0] = 0
    sieve[1] = 0

    if limit > 4:
        sieve[4::2] = b"\x00" * ((limit - 1 - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit - 1) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start::step] = b"\x00" * ((limit - 1 - start) // step + 1)

    return sieve


def termsByPowerOfTwo(limit):
    terms = []
    powerOfTwo = 1

    while powerOfTwo < limit:
        row = []
        powerOfThree = 1
        exponentThree = 0

        while powerOfTwo * powerOfThree < limit:
            row.append((exponentThree, powerOfTwo * powerOfThree))
            powerOfThree *= 3
            exponentThree += 1

        terms.append(list(reversed(row)))
        powerOfTwo *= 2

    return terms


def partitionCounts(limit):
    terms = termsByPowerOfTwo(limit)
    counts = bytearray(limit)
    maxPowerOfTwo = len(terms)

    def search(minPowerOfTwo, maxPowerOfThree, currentSum):
        for exponentTwo in range(minPowerOfTwo, maxPowerOfTwo):
            for exponentThree, value in terms[exponentTwo]:
                if exponentThree >= maxPowerOfThree:
                    continue

                nextSum = currentSum + value

                if nextSum >= limit:
                    continue

                if counts[nextSum] < 2:
                    counts[nextSum] += 1

                search(exponentTwo + 1, exponentThree, nextSum)

    search(0, 100, 0)
    return counts


def specialPartitionPrimeSum(limit=LIMIT):
    counts = partitionCounts(limit)
    primes = primeSieve(limit)

    return sum(number for number in range(2, limit) if primes[number] and counts[number] == 1)


def runTests():
    assert specialPartitionPrimeSum(100) == 233


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = specialPartitionPrimeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
