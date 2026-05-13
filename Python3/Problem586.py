import time
from bisect import bisect_right
from functools import lru_cache
from math import isqrt


FIRST_SPLIT_PRIMES = [
    11, 19, 29, 31, 41, 59, 61, 71, 79, 89,
    101, 109, 131, 139, 149, 151, 179, 181, 191, 199,
]


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0

    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (((limit - start) // prime) + 1)

    return [value for value in range(2, limit + 1) if sieve[value]]


def divisorsGreaterThanOne(number):
    return [divisor for divisor in range(2, number + 1) if number % divisor == 0]


def exponentPartitions(target, minimumDivisor=2):
    if target == 1:
        yield []
        return

    for divisor in range(minimumDivisor, target + 1):
        if target % divisor == 0:
            for rest in exponentPartitions(target // divisor, divisor):
                yield [divisor - 1] + rest


def integerNthRoot(number, exponent):
    if number <= 1:
        return number

    low = 1
    high = int(number ** (1.0 / exponent)) + 3
    while high ** exponent <= number:
        high *= 2

    while low < high:
        mid = (low + high + 1) // 2
        if mid ** exponent <= number:
            low = mid
        else:
            high = mid - 1

    return low


def splitPrimeBound(limit, target):
    bound = 2
    for exponents in exponentPartitions(target):
        for index, exponent in enumerate(exponents):
            otherExponents = sorted(
                exponents[:index] + exponents[index + 1:],
                reverse=True,
            )
            minimalOtherProduct = 1
            for prime, otherExponent in zip(FIRST_SPLIT_PRIMES, otherExponents):
                minimalOtherProduct *= prime ** otherExponent

            if minimalOtherProduct <= limit:
                bound = max(
                    bound,
                    integerNthRoot(limit // minimalOtherProduct, exponent),
                )

    return bound


@lru_cache(maxsize=None)
def minimumRemainingExponentSum(target):
    if target == 1:
        return 0

    return min(
        divisor - 1 + minimumRemainingExponentSum(target // divisor)
        for divisor in divisorsGreaterThanOne(target)
    )


def inertOnlyValues(limit, primes):
    isInertOnly = bytearray(b"\x01") * (limit + 1)
    isInertOnly[0] = 0

    for prime in primes:
        if prime > limit:
            break
        if prime == 5 or prime % 5 in (1, 4):
            isInertOnly[prime:limit + 1:prime] = (
                b"\x00" * (((limit - prime) // prime) + 1)
            )

    return [value for value in range(1, limit + 1) if isInertOnly[value]]


def bruteQuadraticFormCount(limit, representationCount):
    counts = {}
    a = 2
    while a * a + 3 * a + 1 <= limit:
        for b in range(1, a):
            value = a * a + 3 * a * b + b * b
            if value > limit:
                break
            counts[value] = counts.get(value, 0) + 1
        a += 1

    return sum(1 for count in counts.values() if count == representationCount)


def quadraticFormCount(limit, representationCount):
    root = isqrt(limit)
    targetProducts = [2 * representationCount, 2 * representationCount + 1]
    maxSplitPrime = max(
        splitPrimeBound(limit, target)
        for target in targetProducts
    )
    primes = primesUpTo(max(root, maxSplitPrime))
    splitPrimes = [
        prime
        for prime in primes
        if prime <= maxSplitPrime and prime % 5 in (1, 4)
    ]
    inertValues = inertOnlyValues(root, primes)

    neutralFactorCache = {}

    def countNeutralFactors(neutralLimit):
        if neutralLimit in neutralFactorCache:
            return neutralFactorCache[neutralLimit]

        total = 0
        powerOfFive = 1
        while powerOfFive <= neutralLimit:
            total += bisect_right(inertValues, isqrt(neutralLimit // powerOfFive))
            powerOfFive *= 5

        neutralFactorCache[neutralLimit] = total
        return total

    total = 0

    def countSplitProducts(startIndex, target, product):
        nonlocal total

        if target == 1:
            total += countNeutralFactors(limit // product)
            return

        for divisor in divisorsGreaterThanOne(target):
            exponent = divisor - 1
            remainingTarget = target // divisor
            futureExponentSum = minimumRemainingExponentSum(remainingTarget)

            for index in range(startIndex, len(splitPrimes)):
                prime = splitPrimes[index]
                newProduct = product * (prime ** exponent)
                if newProduct > limit:
                    break

                if (
                    remainingTarget != 1
                    and newProduct * ((prime + 1) ** futureExponentSum) > limit
                ):
                    break

                countSplitProducts(index + 1, remainingTarget, newProduct)

    for target in targetProducts:
        countSplitProducts(0, target, 1)

    return total


def runTests():
    for limit in [500, 1_000]:
        for representationCount in range(1, 5):
            assert (
                quadraticFormCount(limit, representationCount)
                == bruteQuadraticFormCount(limit, representationCount)
            )

    assert quadraticFormCount(10 ** 5, 4) == 237
    assert quadraticFormCount(10 ** 8, 6) == 59_517


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = quadraticFormCount(10 ** 15, 40)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
