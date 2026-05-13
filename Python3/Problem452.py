import math
import time
from functools import lru_cache


MODULUS = 1_234_567_891
PROBLEM_LIMIT = 10**9
SIEVE_LIMIT = 1_000_000


def bruteF(limit, length):
    count = 0

    def search(position, product):
        nonlocal count

        if position == length:
            count += 1
            return

        value = 1

        while product * value <= limit:
            search(position + 1, product * value)
            value += 1

    search(0, 1)
    return count


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if isPrime[number]:
            start = number * number
            isPrime[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    primes = [number for number in range(2, limit + 1) if isPrime[number]]
    primeCount = [0] * (limit + 1)
    count = 0

    for number in range(limit + 1):
        if isPrime[number]:
            count += 1
        primeCount[number] = count

    return primes, primeCount


PRIMES, SMALL_PRIME_COUNT = primeSieve(SIEVE_LIMIT)


def integerRoot(number, exponent):
    if exponent == 2:
        return math.isqrt(number)

    low, high = 1, 1
    while high**exponent <= number:
        high *= 2

    low = high // 2
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**exponent <= number:
            low = middle
        else:
            high = middle

    return low


@lru_cache(maxsize=None)
def phiCount(limit, primeIndex):
    if primeIndex == 0:
        return limit
    if primeIndex == 1:
        return limit - limit // 2
    if primeIndex == 2:
        return limit - limit // 2 - limit // 3 + limit // 6

    return phiCount(limit, primeIndex - 1) - phiCount(
        limit // PRIMES[primeIndex - 1], primeIndex - 1
    )


@lru_cache(maxsize=None)
def primeCount(limit):
    if limit <= SIEVE_LIMIT:
        return SMALL_PRIME_COUNT[limit]

    fourthRootCount = primeCount(integerRoot(limit, 4))
    squareRootCount = primeCount(math.isqrt(limit))
    cubeRootCount = primeCount(integerRoot(limit, 3))

    result = phiCount(limit, fourthRootCount)
    result += (
        (squareRootCount + fourthRootCount - 2)
        * (squareRootCount - fourthRootCount + 1)
        // 2
    )

    for index in range(fourthRootCount, squareRootCount):
        prime = PRIMES[index]
        quotient = limit // prime
        result -= primeCount(quotient)

        if index < cubeRootCount:
            nestedLimit = primeCount(math.isqrt(quotient))
            for nestedIndex in range(index, nestedLimit):
                result -= primeCount(quotient // PRIMES[nestedIndex]) - nestedIndex

    return result


def exponentWeights(limit, length):
    maxExponent = limit.bit_length() - 1
    weights = [1] * (maxExponent + 1)
    current = 1

    for exponent in range(1, maxExponent + 1):
        current = (
            current
            * ((length + exponent - 1) % MODULUS)
            % MODULUS
            * pow(exponent, -1, MODULUS)
            % MODULUS
        )
        weights[exponent] = current

    return weights


def tupleProductCount(limit, length):
    weights = exponentWeights(limit, length)
    singlePrimeWeight = weights[1]
    maxExponent = len(weights) - 1

    @lru_cache(maxsize=None)
    def summatory(remainingLimit, primeIndex):
        if remainingLimit < 2:
            return 1

        if primeIndex >= len(PRIMES) or PRIMES[primeIndex] > remainingLimit:
            return 1

        firstPrime = PRIMES[primeIndex]

        if firstPrime * firstPrime > remainingLimit:
            primeChoices = primeCount(remainingLimit) - primeCount(firstPrime - 1)
            return (1 + (primeChoices % MODULUS) * singlePrimeWeight) % MODULUS

        # For k=prod p^e, the exact-product count is prod C(length+e-1,e).
        # Recurse over increasing prime powers; primes above sqrt(limit) can
        # only appear once, so they are counted in one prime-counting call.
        result = 1
        root = math.isqrt(remainingLimit)
        largePrimeChoices = primeCount(remainingLimit) - primeCount(root)
        result = (result + (largePrimeChoices % MODULUS) * singlePrimeWeight) % MODULUS

        index = primeIndex
        while index < len(PRIMES):
            prime = PRIMES[index]
            if prime > root:
                break

            primePower = prime
            exponent = 1

            while primePower <= remainingLimit:
                result = (
                    result
                    + weights[exponent]
                    * summatory(remainingLimit // primePower, index + 1)
                ) % MODULUS
                exponent += 1
                if exponent > maxExponent:
                    break
                primePower *= prime

            index += 1

        return result

    return summatory(limit, 0)


def runTests():
    assert bruteF(10, 10) == 571
    assert tupleProductCount(10, 10) == 571
    assert tupleProductCount(10**6, 10**6) == 252_903_833


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = tupleProductCount(PROBLEM_LIMIT, PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
