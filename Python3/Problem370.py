import math
import time


LIMIT = 25_000_000_000_000


def smallestPrimeFactorSieve(limit):
    factors = list(range(limit + 1))

    for number in range(2, math.isqrt(limit) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def distinctPrimeFactors(number, smallestPrimeFactors):
    factors = []

    while number > 1:
        factor = smallestPrimeFactors[number]
        factors.append(factor)

        while number % factor == 0:
            number //= factor

    return factors


def signedSquarefreeDivisors(primeFactors):
    divisors = [(1, 1)]

    for prime in primeFactors:
        divisors += [(divisor * prime, -sign) for divisor, sign in divisors]

    return divisors


def coprimeCountInRange(lower, upper, signedDivisors):
    total = 0
    beforeLower = lower - 1

    for divisor, sign in signedDivisors:
        total += sign * (upper // divisor - beforeLower // divisor)

    return total


def maxTriangleY(x):
    return (x + math.isqrt(5 * x * x - 1)) // 2


def maxPerimeterY(x, limit):
    discriminant = 4 * limit - 3 * x * x
    if discriminant < 0:
        return x - 1

    return (-x + math.isqrt(discriminant)) // 2


def geometricTriangleCount(limit=LIMIT):
    maxX = math.isqrt(limit // 3) + 2
    smallestPrimeFactors = smallestPrimeFactorSieve(maxX)
    total = 0

    for x in range(1, maxX + 1):
        upperY = min(maxTriangleY(x), maxPerimeterY(x, limit))
        if upperY < x:
            continue

        divisors = signedSquarefreeDivisors(distinctPrimeFactors(x, smallestPrimeFactors))
        y = x

        while y <= upperY:
            perimeter = x * x + x * y + y * y
            quotient = limit // perimeter
            quotientLimit = limit // quotient
            intervalUpper = maxPerimeterY(x, quotientLimit)
            if intervalUpper > upperY:
                intervalUpper = upperY

            total += quotient * coprimeCountInRange(y, intervalUpper, divisors)
            y = intervalUpper + 1

    return total


def runTests():
    assert geometricTriangleCount(10**4) == 6427
    assert geometricTriangleCount(10**5) == 75243
    assert geometricTriangleCount(10**6) == 861805


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = geometricTriangleCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
