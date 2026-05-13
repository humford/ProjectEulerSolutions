import math
import time


MODULUS = 1_000_000_007
DIVISORS = [
    (),
    (1,),
    (1, 2),
    (1, 3),
    (1, 2, 4),
    (1, 5),
    (1, 2, 3, 6),
    (1, 7),
    (1, 2, 4, 8),
    (1, 3, 9),
]
DIVISOR_COUNTS = [len(divisors) for divisors in DIVISORS]
INVERSES = [0] + [pow(n, MODULUS - 2, MODULUS) for n in range(1, 5)]


def buildChunkDigits():
    chunks = [()] * 10_000
    for n in range(1, 10_000):
        digits = []
        remaining = n
        while remaining:
            digit = remaining % 10
            if digit:
                digits.append(digit)
            remaining //= 10
        chunks[n] = tuple(reversed(digits))
    return chunks


CHUNK_DIGITS = buildChunkDigits()


def basePrimesUpTo(limit):
    if limit < 2:
        return []

    sieve = bytearray(limit // 2 + 1)
    root = math.isqrt(limit)
    for i in range(1, root // 2 + 1):
        if sieve[i] == 0:
            prime = 2 * i + 1
            start = prime * prime // 2
            sieve[start::prime] = b"\x01" * (((len(sieve) - start - 1) // prime) + 1)

    primes = [2]
    for i in range(1, len(sieve)):
        if sieve[i] == 0:
            prime = 2 * i + 1
            if prime <= limit:
                primes.append(prime)
    return primes


def primesBelow(limit, segmentOdds=1 << 20):
    if limit <= 2:
        return

    yield 2
    basePrimes = [prime for prime in basePrimesUpTo(math.isqrt(limit - 1)) if prime != 2]
    step = 2 * segmentOdds
    low = 3

    while low < limit:
        high = min(low + step, limit)
        size = (high - low + 1) // 2
        sieve = bytearray(size)

        for prime in basePrimes:
            primeSquared = prime * prime
            if primeSquared >= high:
                break

            start = primeSquared if primeSquared > low else ((low + prime - 1) // prime) * prime
            if start % 2 == 0:
                start += prime

            index = (start - low) // 2
            if index < size:
                sieve[index::prime] = b"\x01" * (((size - index - 1) // prime) + 1)

        for i, isComposite in enumerate(sieve):
            if isComposite == 0:
                yield low + 2 * i

        low += step


def inversionCount(sequence):
    return sum(1 for i in range(len(sequence)) for j in range(i + 1, len(sequence)) if sequence[i] > sequence[j])


def processDigit(digit, greater, counts, expectedInversions):
    counts[digit] += 1
    inverse = INVERSES[DIVISOR_COUNTS[digit]]
    contribution = 0

    for divisor in DIVISORS[digit]:
        contribution += greater[divisor]

    expectedInversions = (expectedInversions + inverse * (contribution % MODULUS)) % MODULUS

    for divisor in DIVISORS[digit]:
        for smaller in range(1, divisor):
            greater[smaller] = (greater[smaller] + inverse) % MODULUS

    return expectedInversions


def dividedSequenceInversionTotal(limit):
    if limit <= 2:
        return 0

    counts = [0] * 10
    greater = [0] * 10
    expectedInversions = 0

    for prime in primesBelow(limit):
        highChunk, lowChunk = divmod(prime, 10_000)
        for digit in CHUNK_DIGITS[highChunk]:
            expectedInversions = processDigit(digit, greater, counts, expectedInversions)
        for digit in CHUNK_DIGITS[lowChunk]:
            expectedInversions = processDigit(digit, greater, counts, expectedInversions)

    sequenceCount = 1
    for digit in range(1, 10):
        count = counts[digit]
        if count:
            sequenceCount = sequenceCount * pow(DIVISOR_COUNTS[digit], count, MODULUS) % MODULUS

    return sequenceCount * expectedInversions % MODULUS


def runTests():
    assert inversionCount("34214") == 5
    assert dividedSequenceInversionTotal(20) == 3_312
    assert dividedSequenceInversionTotal(50) == 338_079_744


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = dividedSequenceInversionTotal(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
