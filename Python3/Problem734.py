import itertools
import time


MODULUS = 1_000_000_007


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0

    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)

    return sieve


def bruteForceBitPrimeTupleCount(limit, tupleSize):
    primes = [number for number, isPrime in enumerate(primeSieve(limit)) if isPrime]
    primeSet = set(primes)

    total = 0
    for values in itertools.product(primes, repeat=tupleSize):
        bitOr = 0
        for value in values:
            bitOr |= value
        if bitOr in primeSet:
            total += 1

    return total


def subsetZetaTransform(values, bitCount):
    for bit in range(bitCount):
        step = 1 << bit
        block = step << 1
        for start in range(0, len(values), block):
            lower = start
            upper = start + step
            for offset in range(step):
                values[upper + offset] += values[lower + offset]


def subsetMobiusTransform(values, bitCount):
    for bit in range(bitCount):
        step = 1 << bit
        block = step << 1
        for start in range(0, len(values), block):
            lower = start
            upper = start + step
            for offset in range(step):
                values[upper + offset] = (values[upper + offset] - values[lower + offset]) % MODULUS


def bitPrimeTupleCount(limit, tupleSize):
    bitCount = limit.bit_length()
    maskCount = 1 << bitCount

    sieve = primeSieve(limit)
    submaskPrimeCounts = [0] * maskCount
    for number, isPrime in enumerate(sieve):
        if isPrime:
            submaskPrimeCounts[number] = 1

    subsetZetaTransform(submaskPrimeCounts, bitCount)

    exactOrCounts = [pow(count, tupleSize, MODULUS) for count in submaskPrimeCounts]
    subsetMobiusTransform(exactOrCounts, bitCount)

    return sum(exactOrCounts[number] for number, isPrime in enumerate(sieve) if isPrime) % MODULUS


def runTests():
    assert 10 | 6 == 14
    assert bruteForceBitPrimeTupleCount(5, 2) == 5
    assert bitPrimeTupleCount(5, 2) == 5
    assert bitPrimeTupleCount(100, 3) == 3_355
    assert bitPrimeTupleCount(1_000, 10) == 2_071_632


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = bitPrimeTupleCount(10**6, 999_983)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
