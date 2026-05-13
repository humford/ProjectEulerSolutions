import math
import time


MODULUS = 1_000_000_000


def mobiusValues(limit):
    values = [1] * (limit + 1)
    values[0] = 0
    primes = []
    isComposite = [False] * (limit + 1)

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            values[number] = -1
        for prime in primes:
            product = number * prime
            if product > limit:
                break
            isComposite[product] = True
            if number % prime == 0:
                values[product] = 0
                break
            values[product] = -values[number]

    return values


def integerRoot(value, exponent):
    guess = int(value ** (1.0 / exponent)) + 3
    while pow(guess, exponent) <= value:
        guess *= 2

    low = 1
    high = guess
    while low + 1 < high:
        middle = (low + high) // 2
        if pow(middle, exponent) <= value:
            low = middle
        else:
            high = middle
    return low


def maxExponent(limit):
    exponent = limit.bit_length() - 1
    while pow(2, exponent + 1) <= limit:
        exponent += 1
    while pow(2, exponent) > limit:
        exponent -= 1
    return exponent


def primitiveBaseCount(limit, mobius):
    if limit < 2:
        return 0

    return sum(
        mobius[exponent] * (integerRoot(limit, exponent) - 1)
        for exponent in range(1, maxExponent(limit) + 1)
    )


def reducedExponentPairCount(maxDenominator, maxNumerator):
    return sum(
        1
        for denominator in range(1, maxDenominator + 1)
        for numerator in range(1, maxNumerator + 1)
        if math.gcd(denominator, numerator) == 1
    )


def protoLogDistinctValueCount(limit):
    largestExponent = maxExponent(limit)
    mobius = mobiusValues(largestExponent)

    roots = [
        0,
        *(
            integerRoot(limit, exponent)
            for exponent in range(1, largestExponent + 2)
        ),
    ]
    primitiveCounts = [0] * (largestExponent + 1)
    for exponent in range(1, largestExponent + 1):
        primitiveCounts[exponent] = (
            primitiveBaseCount(roots[exponent], mobius)
            - primitiveBaseCount(roots[exponent + 1], mobius)
        )

    reducedPairCounts = [
        [0] * (largestExponent + 1)
        for _ in range(largestExponent + 1)
    ]
    for denominatorLimit in range(1, largestExponent + 1):
        for numeratorLimit in range(1, largestExponent + 1):
            reducedPairCounts[denominatorLimit][numeratorLimit] = (
                reducedExponentPairCount(denominatorLimit, numeratorLimit)
            )

    total = reducedPairCounts[largestExponent][largestExponent]
    for denominatorLimit in range(1, largestExponent + 1):
        for numeratorLimit in range(1, largestExponent + 1):
            orderedBasePairs = (
                primitiveCounts[denominatorLimit]
                * primitiveCounts[numeratorLimit]
            )
            if denominatorLimit == numeratorLimit:
                orderedBasePairs -= primitiveCounts[denominatorLimit]
            total += (
                orderedBasePairs
                * reducedPairCounts[denominatorLimit][numeratorLimit]
            )

    return total % MODULUS


def runTests():
    assert protoLogDistinctValueCount(5) == 13
    assert protoLogDistinctValueCount(10) == 69
    assert protoLogDistinctValueCount(100) == 9_607
    assert protoLogDistinctValueCount(10_000) == 99_959_605


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = protoLogDistinctValueCount(10 ** 18) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
