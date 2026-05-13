import math
import time
from array import array


MODULUS = 1_000_000_007


def primeCount(limit):
    count = 0

    for number in range(2, limit + 1):
        isPrime = True

        for divisor in range(2, int(number**0.5) + 1):
            if number % divisor == 0:
                isPrime = False
                break

        if isPrime:
            count += 1

    return count


def outcomeCount(throws):
    primeLimit = primeCount(throws)
    return 6 * sum(
        math.comb(throws - 1, repeats) * 5 ** (throws - 1 - repeats)
        for repeats in range(primeLimit + 1)
    )


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit // 2 + 1)

    if limit >= 1:
        sieve[0] = 0

    for number in range(3, int(limit**0.5) + 1, 2):
        if sieve[number // 2]:
            start = number * number // 2
            sieve[start::number] = b"\x00" * (
                ((limit // 2) - start) // number + 1
            )

    return sieve


def isPrime(number, oddPrimeSieve):
    return number == 2 or (
        number > 2 and number % 2 == 1 and oddPrimeSieve[number // 2]
    )


def modularInverses(limit):
    inverses = array("I", [0]) * (limit + 1)
    inverses[1] = 1

    for number in range(2, limit + 1):
        inverses[number] = (
            MODULUS - (MODULUS // number) * inverses[MODULUS % number] % MODULUS
        ) % MODULUS

    return inverses


def S(limit):
    oddPrimeSieve = primeSieve(limit)
    inverses = modularInverses(limit)
    partialSum = 1
    topTerm = 1
    primeTotal = 0
    total = 6

    for throws in range(1, limit):
        basePartialSum = (6 * partialSum - topTerm) % MODULUS

        if isPrime(throws + 1, oddPrimeSieve):
            primeTotal += 1
            topTerm = topTerm * throws % MODULUS * inverses[primeTotal] % MODULUS
            partialSum = (basePartialSum + topTerm) % MODULUS
        else:
            topTerm = (
                topTerm
                * 5
                % MODULUS
                * throws
                % MODULUS
                * inverses[throws - primeTotal]
                % MODULUS
            )
            partialSum = basePartialSum

        total = (total + 6 * partialSum) % MODULUS

    return total


def runTests():
    assert outcomeCount(3) == 216
    assert outcomeCount(4) == 1290
    assert outcomeCount(11) == 361912500
    assert outcomeCount(24) == 4727547363281250000
    assert S(50) == 832833871


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(50_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
