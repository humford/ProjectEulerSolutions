import time
from bisect import bisect_left
from math import isqrt


TARGET = 1_000_000


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))
    for number in range(2, isqrt(limit) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number
    return factors


def factorize(number, factors):
    factorization = []
    while number > 1:
        prime = factors[number]
        exponent = 0
        while number % prime == 0:
            number //= prime
            exponent += 1
        factorization.append((prime, exponent))
    return factorization


def squareDivisorsUpToRoot(root, factorization):
    divisors = [1]
    for prime, exponent in factorization:
        powers = [1]
        power = 1
        for _ in range(2 * exponent):
            power *= prime
            powers.append(power)

        newDivisors = []
        for divisor in divisors:
            for power in powers[1:]:
                value = divisor * power
                if value > root:
                    break
                newDivisors.append(value)
        divisors += newDivisors

    divisors.sort()
    return divisors


def maximalAreaPerimeterSum(limit):
    factors = smallestPrimeFactors(limit)
    total = 0
    localIsqrt = isqrt
    localBisectLeft = bisect_left
    localFactorize = factorize
    localDivisors = squareDivisorsUpToRoot

    for area in range(1, limit + 1):
        areaSquared = area * area
        divisors = localDivisors(area, localFactorize(area, factors))
        divisorCount = len(divisors)

        for tIndex, smallest in enumerate(divisors):
            remainingAfterSmallest = areaSquared // smallest

            for wIndex in range(tIndex, divisorCount):
                secondSmallest = divisors[wIndex]
                if secondSmallest > remainingAfterSmallest:
                    break
                if remainingAfterSmallest % secondSmallest:
                    continue

                remaining = remainingAfterSmallest // secondSmallest
                largestMiddleMax = localIsqrt(remaining)
                if largestMiddleMax < secondSmallest:
                    continue
                if largestMiddleMax > area:
                    largestMiddleMax = area

                lowerSum = secondSmallest + smallest
                discriminant = lowerSum * lowerSum + 4 * remaining
                largestMiddleMin = (localIsqrt(discriminant) - lowerSum) // 2 + 1
                if largestMiddleMin < secondSmallest:
                    largestMiddleMin = secondSmallest
                if largestMiddleMin > largestMiddleMax:
                    continue

                startIndex = localBisectLeft(divisors, largestMiddleMin)
                for vIndex in range(startIndex, divisorCount):
                    largestMiddle = divisors[vIndex]
                    if largestMiddle > largestMiddleMax:
                        break
                    if remaining % largestMiddle:
                        continue

                    largest = remaining // largestMiddle
                    if largest < largestMiddle:
                        continue
                    if largest >= largestMiddle + lowerSum:
                        continue

                    perimeter = largest + largestMiddle + lowerSum
                    if perimeter & 1 == 0:
                        total += perimeter

    return total


def runTests():
    assert maximalAreaPerimeterSum(10) == 186
    assert maximalAreaPerimeterSum(100) == 23_238


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximalAreaPerimeterSum(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
