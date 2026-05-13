import collections
import math
import time


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return [number for number, isPrime in enumerate(sieve) if isPrime]


def factorialPrimeExponents(limit):
    exponents = {}
    for prime in primesUpTo(limit):
        exponent = 0
        value = limit
        while value:
            value //= prime
            exponent += value
        exponents[prime] = exponent
    return exponents


def factorizeSmall(number):
    exponents = {}
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            exponents[divisor] = exponents.get(divisor, 0) + 1
            number //= divisor
        divisor += 1 if divisor == 2 else 2
    if number > 1:
        exponents[number] = exponents.get(number, 0) + 1
    return exponents


def splitDivisibilityCountFromExponentsBrute(exponents):
    values = list(exponents.values())
    matchingDivisors = 0

    def search(index, divisorCountA, divisorCountB):
        nonlocal matchingDivisors
        if index == len(values):
            if divisorCountA == divisorCountB:
                matchingDivisors += 1
            return

        exponent = values[index]
        for split in range(exponent + 1):
            search(index + 1, divisorCountA * (split + 1), divisorCountB * (exponent - split + 1))

    search(0, 1, 1)
    isSquare = all(exponent % 2 == 0 for exponent in values)
    return (matchingDivisors + (1 if isSquare else 0)) // 2


def smallestPrimeFactorSieve(limit):
    factors = list(range(limit + 1))
    if limit >= 1:
        factors[1] = 1
    for number in range(2, math.isqrt(limit) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number
    return factors


def factorVector(number, spf, primes):
    indexes = {prime: index for index, prime in enumerate(primes)}
    vector = [0] * len(primes)
    hasLargePrime = False

    while number > 1:
        prime = spf[number]
        count = 0
        while number % prime == 0:
            number //= prime
            count += 1
        if prime in indexes:
            vector[indexes[prime]] = count
        if prime > 47:
            hasLargePrime = True

    return tuple(vector), hasLargePrime


def vectorAdd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def vectorSub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def precomputeSplitVectors(limit, lowPrimes, highPrimes):
    spf = smallestPrimeFactorSieve(limit)
    lowVectors = [(0,) * len(lowPrimes)] * (limit + 1)
    highVectors = [(0,) * len(highPrimes)] * (limit + 1)
    hasLargePrime = [False] * (limit + 1)

    for number in range(1, limit + 1):
        lowVectors[number], lowBig = factorVector(number, spf, lowPrimes)
        highVectors[number], highBig = factorVector(number, spf, highPrimes)
        hasLargePrime[number] = lowBig or highBig

    return lowVectors, highVectors, hasLargePrime


def convolve2D(distribution, deltas):
    result = collections.defaultdict(int)
    for (a, b), count in distribution.items():
        for deltaA, deltaB in deltas:
            result[(a + deltaA, b + deltaB)] += count
    return dict(result)


def splitDivisibilityCount100Factorial():
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    highPrimes = [29, 31, 37, 41, 43, 47]
    lowVectors, highVectors, hasLargePrime = precomputeSplitVectors(99, lowPrimes, highPrimes)

    factorialExponents = factorialPrimeExponents(100)
    mediumPrimes = [5, 7, 11, 13, 17, 19, 23]
    mediumExponents = [factorialExponents[prime] for prime in mediumPrimes]

    optionsByExponent = {}
    for exponent in set(mediumExponents):
        options = []
        for split in range(exponent + 1):
            numerator = split + 1
            denominator = exponent - split + 1
            diff = vectorSub(lowVectors[numerator], lowVectors[denominator])
            options.append((diff[0], diff[1], diff[2:]))
        optionsByExponent[exponent] = options

    distribution = {(0,) * 7: {(0, 0): 1}}
    for exponent in mediumExponents:
        newDistribution = {}
        for outerVector, inner in distribution.items():
            for (d2, d3), count in inner.items():
                for delta2, delta3, deltaOuter in optionsByExponent[exponent]:
                    nextOuter = vectorAdd(outerVector, deltaOuter)
                    nextInnerKey = (d2 + delta2, d3 + delta3)
                    nextInner = newDistribution.setdefault(nextOuter, {})
                    nextInner[nextInnerKey] = nextInner.get(nextInnerKey, 0) + count
        distribution = newDistribution

    smallDistribution = {(0, 0): 1}
    for _ in range(10):
        smallDistribution = convolve2D(smallDistribution, [(1, 0), (-1, 0)])
    for _ in range(4):
        smallDistribution = convolve2D(smallDistribution, [(0, 1), (0, 0), (0, -1)])
    for _ in range(2):
        smallDistribution = convolve2D(smallDistribution, [(-2, 0), (1, -1), (-1, 1), (2, 0)])

    totalMatchingDivisors = 0
    threeSplitInfo = []
    for numerator3 in range(1, 50):
        denominator3 = 50 - numerator3
        threeSplitInfo.append(
            (
                vectorSub(lowVectors[numerator3], lowVectors[denominator3]),
                vectorSub(highVectors[numerator3], highVectors[denominator3]),
            )
        )

    for numerator2 in range(1, 99):
        denominator2 = 99 - numerator2
        if hasLargePrime[numerator2] or hasLargePrime[denominator2]:
            continue

        lowDiff2 = vectorSub(lowVectors[numerator2], lowVectors[denominator2])
        highDiff2 = vectorSub(highVectors[numerator2], highVectors[denominator2])

        for lowDiff3, highDiff3 in threeSplitInfo:
            if any(value != 0 for value in vectorAdd(highDiff2, highDiff3)):
                continue

            lowDiff = vectorAdd(lowDiff2, lowDiff3)
            targetOuter = tuple(-value for value in lowDiff[2:])
            inner = distribution.get(targetOuter)
            if inner is None:
                continue

            target2 = -lowDiff[0]
            target3 = -lowDiff[1]
            subtotal = 0
            for (small2, small3), smallCount in smallDistribution.items():
                subtotal += inner.get((target2 - small2, target3 - small3), 0) * smallCount
            totalMatchingDivisors += subtotal

    return totalMatchingDivisors // 2


def splitDivisibilityCount(number):
    return splitDivisibilityCountFromExponentsBrute(factorizeSmall(number))


def runTests():
    assert splitDivisibilityCount(48) == 1
    assert splitDivisibilityCountFromExponentsBrute(factorialPrimeExponents(10)) == 3


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = splitDivisibilityCount100Factorial()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
