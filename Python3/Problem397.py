import math
import time


LIMIT_K = 10**6
LIMIT_X = 10**9


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))

    for number in range(2, math.isqrt(limit) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def factorization(number, smallestFactors):
    factors = []

    while number > 1:
        prime = smallestFactors[number]
        exponent = 0

        while number % prime == 0:
            number //= prime
            exponent += 1

        factors.append((prime, exponent))

    return factors


def divisorsFromFactors(factors):
    divisors = [1]

    for prime, exponent in factors:
        nextDivisors = []
        power = 1

        for _ in range(exponent + 1):
            for divisor in divisors:
                nextDivisors.append(divisor * power)

            power *= prime

        divisors = nextDivisors

    return divisors


def angleVertexCount(low, high, firstSum, secondSum, denominator):
    if low > high:
        return 0

    if denominator > 0:
        beforeFirst = max(0, min(high, (firstSum - 1) // 2) - low + 1)
        afterSecond = max(0, high - max(low, secondSum // 2 + 1) + 1)
        return beforeFirst + afterSecond

    first = max(low, firstSum // 2 + 1)
    last = min(high, (secondSum - 1) // 2)

    return max(0, last - first + 1)


def duplicateTriangleCount(limitK, limitX, smallestFactors):
    total = 0

    for k in range(1, limitK + 1):
        square = k * k
        divisors = divisorsFromFactors(
            [(prime, 2 * exponent) for prime, exponent in factorization(k, smallestFactors)]
        )
        triangles = set()

        for positiveSum in divisors:
            negativeSum = -square // positiveSum
            firstWeight = square + negativeSum * negativeSum
            secondWeight = square + positiveSum * positiveSum

            if firstWeight == secondWeight:
                candidates = (0,)
            else:
                a = 4 * (firstWeight - secondWeight)
                b = -4 * (firstWeight * negativeSum - secondWeight * positiveSum)
                c = (
                    firstWeight * negativeSum * negativeSum
                    - secondWeight * positiveSum * positiveSum
                )
                discriminant = b * b - 4 * a * c
                root = math.isqrt(discriminant)

                if root * root != discriminant:
                    continue

                candidates = []

                for numerator in (-b + root, -b - root):
                    denominator = 2 * a

                    if numerator % denominator == 0:
                        candidates.append(numerator // denominator)

            for vertex in candidates:
                triangle = tuple(
                    sorted((vertex, negativeSum - vertex, positiveSum - vertex))
                )

                if (
                    triangle[0] < triangle[1] < triangle[2]
                    and triangle[0] >= -limitX
                    and triangle[2] <= limitX
                ):
                    triangles.add(triangle)

        total += len(triangles)

    return total


def exactTriangleCount(limitK, limitX):
    smallestFactors = smallestPrimeFactors(limitK)
    total = 0

    for k in range(1, limitK + 1):
        factors = []
        hasTwo = False

        for prime, exponent in factorization(k, smallestFactors):
            exponent *= 2

            if prime == 2:
                exponent += 1
                hasTwo = True

            factors.append((prime, exponent))

        if not hasTwo:
            factors.append((2, 1))

        square = k * k
        pairs = set()

        for positiveDivisor in divisorsFromFactors(factors):
            for divisor in (positiveDivisor, -positiveDivisor):
                firstSum = k - divisor
                secondSum = 2 * square // divisor - k

                if firstSum != secondSum:
                    pairs.add(tuple(sorted((firstSum, secondSum))))

                firstSum = divisor - k
                secondSum = k - 2 * square // divisor

                if firstSum != secondSum:
                    pairs.add(tuple(sorted((firstSum, secondSum))))

        for firstSum, secondSum in pairs:
            if firstSum < -2 * limitX or secondSum > 2 * limitX:
                continue

            denominator = square + firstSum * secondSum

            if denominator == 0:
                continue

            low = max(-limitX, firstSum - limitX, secondSum - limitX)
            high = min(limitX, firstSum + limitX, secondSum + limitX)
            total += angleVertexCount(low, high, firstSum, secondSum, denominator)

    return total - duplicateTriangleCount(limitK, limitX, smallestFactors)


def triangleCount(limitK=LIMIT_K, limitX=LIMIT_X):
    return exactTriangleCount(limitK, limitX)


def runTests():
    assert triangleCount(1, 10) == 41
    assert triangleCount(10, 100) == 12492


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangleCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
