import functools
import math
import time


LIMIT = 10**10


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))

    for number in range(2, math.isqrt(limit) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def squarefreeAndSquareParts(limit):
    factors = smallestPrimeFactors(limit)
    squarefree = [0] * (limit + 1)
    square_root = [0] * (limit + 1)
    squarefree[1] = 1
    square_root[1] = 1

    for number in range(2, limit + 1):
        remaining = number
        squarefree_part = 1
        square_root_part = 1

        while remaining > 1:
            prime = factors[remaining]
            exponent = 0

            while remaining % prime == 0:
                remaining //= prime
                exponent += 1

            if exponent & 1:
                squarefree_part *= prime
            square_root_part *= prime ** (exponent // 2)

        squarefree[number] = squarefree_part
        square_root[number] = square_root_part

    return squarefree, square_root


@functools.lru_cache(None)
def fundamentalPellSolution(discriminant):
    root = math.isqrt(discriminant)
    previous_m = 0
    previous_d = 1
    coefficient = root
    numerator_previous = 1
    numerator = coefficient
    denominator_previous = 0
    denominator = 1

    while numerator * numerator - discriminant * denominator * denominator != 1:
        previous_m = previous_d * coefficient - previous_m
        previous_d = (discriminant - previous_m * previous_m) // previous_d
        coefficient = (root + previous_m) // previous_d
        numerator_previous, numerator = (
            numerator,
            coefficient * numerator + numerator_previous,
        )
        denominator_previous, denominator = (
            denominator,
            coefficient * denominator + denominator_previous,
        )

    return numerator, denominator


def squarePivots(limit):
    maximum_m = (math.isqrt(1 + 2 * limit) - 1) // 2
    squarefree, square_root = squarefreeAndSquareParts(maximum_m + 2)
    pivots = set()

    for m in range(1, maximum_m + 1):
        discriminant = squarefree[m] * squarefree[m + 1]
        x1, y1 = fundamentalPellSolution(discriminant)
        x, y = x1, y1
        multiplier = discriminant * square_root[m] * square_root[m + 1]

        while True:
            t = multiplier * y
            twice_k = m * (x + 1) + t
            if twice_k > 2 * limit:
                break

            twice_n = (m + 1) * (x - 1) + t
            if twice_n >= twice_k and twice_k % 2 == 0 and twice_n % 2 == 0:
                pivots.add(twice_k // 2)

            x, y = x1 * x + discriminant * y1 * y, x1 * y + y1 * x

    return pivots


def squarePivotSum(limit):
    return sum(squarePivots(limit))


def bruteSquarePivots(limit):
    prefix = [0]
    for number in range(1, 3 * limit + 1):
        prefix.append(prefix[-1] + number * number)

    pivots = set()
    for k in range(1, limit + 1):
        for m in range(1, k + 1):
            left = prefix[k] - prefix[k - m - 1]
            n = k
            while n + m < len(prefix):
                right = prefix[n + m] - prefix[n]
                if right == left:
                    pivots.add(k)
                    break
                if right > left:
                    break
                n += 1

    return pivots


def runTests():
    pivots = squarePivots(120)
    assert {4, 21, 24, 110}.issubset(pivots)
    assert pivots == bruteSquarePivots(120)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squarePivotSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
