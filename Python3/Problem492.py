import math
import time


LUCAS_P = 11
QUADRATIC_RESIDUES_13 = {1, 3, 4, 9, 10, 12}


def sequenceValue(n, modulus=None):
    value = 1
    for _ in range(1, n):
        value = 6 * value * value + 10 * value + 3
        if modulus is not None:
            value %= modulus
    return value


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


def segmentedPrimes(start, stop, basePrimes):
    if stop < 2 or stop < start:
        return

    if start <= 2 <= stop:
        yield 2

    firstOdd = start | 1
    if firstOdd > stop:
        return

    segment = bytearray(b"\x01") * ((stop - firstOdd) // 2 + 1)

    for prime in basePrimes[1:]:
        square = prime * prime
        if square > stop:
            break

        first = max(square, ((firstOdd + prime - 1) // prime) * prime)
        if first % 2 == 0:
            first += prime

        index = (first - firstOdd) // 2
        segment[index::prime] = b"\x00" * ((len(segment) - index - 1) // prime + 1)

    for index, isPrime in enumerate(segment):
        if isPrime:
            yield firstOdd + 2 * index


def lucasUPair(index, modulus):
    if index == 0:
        return 0, 1

    u, nextU = 0, 1
    mask = 1 << (index.bit_length() - 1)

    while mask:
        lucasV = (2 * nextU - LUCAS_P * u) % modulus
        doubledU = u * lucasV % modulus
        doubledNextU = (nextU * lucasV - 1) % modulus

        if index & mask:
            u, nextU = doubledNextU, (LUCAS_P * doubledNextU - doubledU) % modulus
        else:
            u, nextU = doubledU, doubledNextU

        mask >>= 1

    return u, nextU


def lucasV(index, modulus):
    u, nextU = lucasUPair(index, modulus)
    return (2 * nextU - LUCAS_P * u) % modulus


def sequenceValueModPrime(n, prime):
    if prime in (2, 3):
        return 1 % prime
    if prime == 13:
        return sequenceValue(n, prime)

    legendre117 = 1 if prime % 13 in QUADRATIC_RESIDUES_13 else -1
    orderMultiple = prime - legendre117
    lucasIndex = pow(2, n - 1, orderMultiple)
    transformed = lucasV(lucasIndex, prime)
    return (transformed - 5) * pow(6, -1, prime) % prime


def primeSequenceSum(x, y, n):
    basePrimes = primeSieve(math.isqrt(x + y) + 1)
    total = 0
    for prime in segmentedPrimes(x, x + y, basePrimes):
        total += sequenceValueModPrime(n, prime)
    return total


def runTests():
    assert sequenceValue(3) == 2_359
    assert sequenceValue(6) == 269_221_280_981_320_216_750_489_044_576_319
    assert sequenceValue(6, 1_000_000_007) == 203_064_689
    assert sequenceValue(100, 1_000_000_007) == 456_482_974
    assert sequenceValueModPrime(6, 1_000_000_007) == 203_064_689
    assert sequenceValueModPrime(100, 1_000_000_007) == 456_482_974
    assert primeSequenceSum(10 ** 9, 10 ** 3, 10 ** 3) == 23_674_718_882
    assert primeSequenceSum(10 ** 9, 10 ** 3, 10 ** 15) == 20_731_563_854


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeSequenceSum(10 ** 9, 10 ** 7, 10 ** 15)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
