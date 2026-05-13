import functools
import math
import time


MODULUS = 1_000_000_007


def integerCubeRoot(number):
    root = int(round(number ** (1.0 / 3.0)))
    while (root + 1) ** 3 <= number:
        root += 1
    while root ** 3 > number:
        root -= 1
    return root


def floorSumRange(number, start, stop):
    total = 0
    divisor = start
    while divisor <= stop:
        quotient = number // divisor
        lastDivisor = min(stop, number // quotient)
        total += quotient * (lastDivisor - divisor + 1)
        divisor = lastDivisor + 1
    return total


def arithmeticSum(start, stop):
    count = stop - start + 1
    return (start + stop) * count // 2


@functools.lru_cache(None)
def baseTupleCountAndLengthSum(limit, minimum):
    if limit < minimum:
        return 0, 0

    if minimum * minimum > limit:
        count = (limit - minimum + 1) % MODULUS
        return count, count

    count = limit - minimum + 1
    lengthSum = count
    squareRoot = math.isqrt(limit)

    if minimum * minimum * minimum > limit:
        rangeStart = minimum
        if rangeStart <= squareRoot:
            floorSum = floorSumRange(limit, rangeStart, squareRoot)
            factorSum = arithmeticSum(rangeStart, squareRoot)
            baseCount = floorSum - factorSum + (squareRoot - rangeStart + 1)
            count += baseCount
            lengthSum += 2 * baseCount
        return count % MODULUS, lengthSum % MODULUS

    cubeRoot = integerCubeRoot(limit)
    recursiveStop = min(cubeRoot, squareRoot)

    for firstFactor in range(minimum, recursiveStop + 1):
        subCount, subLengthSum = baseTupleCountAndLengthSum(limit // firstFactor, firstFactor)
        count += subCount
        lengthSum += subLengthSum + subCount

    rangeStart = max(minimum, recursiveStop + 1)
    if rangeStart <= squareRoot:
        floorSum = floorSumRange(limit, rangeStart, squareRoot)
        factorSum = arithmeticSum(rangeStart, squareRoot)
        baseCount = floorSum - factorSum + (squareRoot - rangeStart + 1)
        count += baseCount
        lengthSum += 2 * baseCount

    return count % MODULUS, lengthSum % MODULUS


@functools.lru_cache(None)
def orderedFactorisationsExact(number, factors, minimum):
    if factors == 1:
        return 1 if number >= minimum else 0

    total = 0
    firstFactor = minimum
    while firstFactor ** factors <= number:
        if number % firstFactor == 0:
            total += orderedFactorisationsExact(number // firstFactor, factors - 1, firstFactor)
        firstFactor += 1
    return total


def orderedFactorisationTotalBrute(limit, maxFactors):
    orderedFactorisationsExact.cache_clear()
    return sum(
        orderedFactorisationsExact(number, factors, 1)
        for number in range(1, limit + 1)
        for factors in range(1, maxFactors + 1)
    )


def orderedFactorisationTotal(limit, maxFactors):
    if limit <= 0 or maxFactors <= 0:
        return 0

    maximumBaseLength = limit.bit_length() - 1
    if maxFactors < maximumBaseLength:
        raise ValueError("This implementation assumes maxFactors >= floor(log2(limit))")

    baseTupleCountAndLengthSum.cache_clear()
    baseCount, baseLengthSum = baseTupleCountAndLengthSum(limit, 2)

    # n=1 contributes one all-ones tuple for each length. Every other tuple is
    # a base tuple of factors at least 2, padded by any number of leading ones.
    return (maxFactors % MODULUS + ((maxFactors + 1) % MODULUS) * baseCount - baseLengthSum) % MODULUS


def runTests():
    assert orderedFactorisationTotalBrute(10, 10) == 153
    assert orderedFactorisationTotal(10, 10) == 153
    assert orderedFactorisationTotal(100, 100) == 35_384


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = orderedFactorisationTotal(10**10, 10**10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
