from math import isqrt
from multiprocessing import cpu_count, get_context
import time


MODULUS = 1_111_211_113
TARGET_N = 10_000

WORKER_INVERSES = None
WORKER_WEIGHTS = None


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    primes = []

    for value in range(2, limit + 1):
        if sieve[value]:
            primes.append(value)
            start = value * value
            if start <= limit:
                sieve[start::value] = b"\x00" * (((limit - start) // value) + 1)

    return primes


def triangularImageSizePrimePower(prime, exponent):
    if prime == 2:
        return 1 << exponent

    size = (prime + 1) // 2
    for currentExponent in range(2, exponent + 1):
        if currentExponent % 2 == 0:
            size = prime * size - (prime - 1)
        else:
            size = prime * size - (prime - 1) // 2

    return size


def triangularImageSize(value):
    remaining = value
    result = 1
    prime = 2

    while prime * prime <= remaining:
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            result *= triangularImageSizePrimePower(prime, exponent)
        prime += 1 if prime == 2 else 2

    if remaining > 1:
        result *= triangularImageSizePrimePower(remaining, 1)

    return result


def triangularImageSizeBrute(modulus):
    return len({
        index * (index + 1) // 2 % modulus
        for index in range(2 * modulus)
    })


def primePowerOptions(maxPeriod):
    options = []
    for prime in primeSieve(2 * maxPeriod):
        values = []
        exponent = 1
        primePower = prime

        while True:
            imageSize = triangularImageSizePrimePower(prime, exponent)
            if imageSize > maxPeriod:
                break
            values.append((primePower, imageSize))
            exponent += 1
            primePower *= prime

        options.append(values)

    return options


def generateAdmissibleModuli(maxPeriod):
    options = primePowerOptions(maxPeriod)
    moduli = []

    def search(startIndex, modulus, imageSize):
        moduli.append((modulus, imageSize))
        for index in range(startIndex, len(options)):
            for primePower, primePowerImageSize in options[index]:
                nextImageSize = imageSize * primePowerImageSize
                if nextImageSize > maxPeriod:
                    break
                search(index + 1, modulus * primePower, nextImageSize)

    search(0, 1, 1)
    return moduli


def mobiusValues(limit):
    mobius = [0] * (limit + 1)
    mobius[1] = 1
    primes = []
    composite = bytearray(limit + 1)

    for value in range(2, limit + 1):
        if not composite[value]:
            primes.append(value)
            mobius[value] = -1
        for prime in primes:
            multiple = value * prime
            if multiple > limit:
                break
            composite[multiple] = 1
            if value % prime == 0:
                mobius[multiple] = 0
                break
            mobius[multiple] = -mobius[value]

    return mobius


def workerInit(inverses, weights):
    global WORKER_INVERSES
    global WORKER_WEIGHTS
    WORKER_INVERSES = inverses
    WORKER_WEIGHTS = weights


def chunkContribution(chunk):
    inverses = WORKER_INVERSES
    weights = WORKER_WEIGHTS
    maxPeriod = len(weights) - 1
    total = 0

    for modulus, imageSize in chunk:
        remainingPositions = modulus - imageSize
        binomial = 1
        total += weights[imageSize]
        total %= MODULUS

        for extraBoundaries in range(1, maxPeriod - imageSize + 1):
            binomial = (
                binomial
                * ((remainingPositions - extraBoundaries + 1) % MODULUS)
                % MODULUS
                * inverses[extraBoundaries]
                % MODULUS
            )
            total = (
                total
                + binomial * weights[imageSize + extraBoundaries]
            ) % MODULUS

    return total


def modularInverses(limit):
    inverses = [0] * (limit + 1)
    inverses[1] = 1

    for value in range(2, limit + 1):
        inverses[value] = (
            MODULUS
            - (MODULUS // value) * inverses[MODULUS % value] % MODULUS
        )

    return inverses


def primitiveClockCount(maxPeriod, processes=None):
    moduli = generateAdmissibleModuli(maxPeriod)
    moduli.sort(key=lambda item: item[1])

    mobius = mobiusValues(maxPeriod)
    mertens = [0] * (maxPeriod + 1)
    for value in range(1, maxPeriod + 1):
        mertens[value] = mertens[value - 1] + mobius[value]

    weights = [0] * (maxPeriod + 1)
    for periodLength in range(1, maxPeriod + 1):
        weights[periodLength] = mertens[maxPeriod // periodLength] % MODULUS

    inverses = modularInverses(maxPeriod)

    if processes is None:
        processes = min(8, cpu_count() or 1)
    processes = max(1, min(processes, len(moduli)))

    if processes == 1:
        workerInit(inverses, weights)
        return chunkContribution(moduli) % MODULUS

    try:
        context = get_context("fork")
    except ValueError:
        workerInit(inverses, weights)
        return chunkContribution(moduli) % MODULUS

    chunks = [moduli[index::processes] for index in range(processes)]
    with context.Pool(
        processes,
        initializer=workerInit,
        initargs=(inverses, weights),
    ) as pool:
        return sum(pool.map(chunkContribution, chunks)) % MODULUS


def solve():
    return primitiveClockCount(TARGET_N)


def runTests():
    for modulus in range(1, 80):
        assert triangularImageSize(modulus) == triangularImageSizeBrute(modulus)

    assert primitiveClockCount(3, processes=1) == 3
    assert primitiveClockCount(4, processes=1) == 7
    assert primitiveClockCount(10, processes=1) == 561


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 451_822_602
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
