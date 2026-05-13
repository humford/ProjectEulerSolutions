import math
import time


def rawDenominator(numerator, denominator):
    denominatorSquared = denominator * denominator
    numeratorSquared = numerator * numerator
    return (5 * denominatorSquared - numeratorSquared) * (
        5 * denominatorSquared
        + numeratorSquared
        - 5 * numerator * denominator
    )


def firstNumeratorWithinLimit(denominator, limit):
    if rawDenominator(denominator - 1, denominator) > limit:
        return denominator

    low = 1
    high = denominator - 1
    while low < high:
        middle = (low + high) // 2
        if rawDenominator(middle, denominator) <= limit:
            high = middle
        else:
            low = middle + 1

    return low


def reducedSides(numerator, denominator):
    divisor = 5 if numerator % 5 == 0 else 1
    denominatorSquared = denominator * denominator
    numeratorSquared = numerator * numerator

    oddSide = (5 * denominatorSquared - numeratorSquared) // divisor
    halfEvenSide = (
        5 * denominatorSquared
        + numeratorSquared
        - 5 * numerator * denominator
    ) // divisor
    hypotenuse = (
        5 * denominatorSquared
        + numeratorSquared
        - 4 * numerator * denominator
    ) // divisor
    return oddSide, halfEvenSide, hypotenuse


def canonicalTriplet(numerator, denominator):
    oddSide, halfEvenSide, hypotenuse = reducedSides(numerator, denominator)
    evenSide = 2 * halfEvenSide
    smallerSide = min(oddSide, evenSide)
    largerSide = max(oddSide, evenSide)

    return (
        oddSide * halfEvenSide,
        hypotenuse * smallerSide,
        hypotenuse * largerSide,
    )


def canonicalTripletCount(limit):
    total = 0
    gcd = math.gcd
    maxDenominator = math.isqrt(math.isqrt(25 * limit // 4)) + 3

    for denominator in range(2, maxDenominator + 1):
        denominatorSquared = denominator * denominator

        firstNumerator = firstNumeratorWithinLimit(denominator, limit)
        for numerator in range(firstNumerator, denominator):
            if (numerator + denominator) & 1 and numerator % 5 and gcd(numerator, denominator) == 1:
                numeratorSquared = numerator * numerator
                first = 5 * denominatorSquared - numeratorSquared
                second = (
                    5 * denominatorSquared
                    + numeratorSquared
                    - 5 * numerator * denominator
                )
                total += limit // (first * second)

        if denominator % 5 == 0:
            continue

        firstNumerator = firstNumeratorWithinLimit(denominator, 25 * limit)
        firstMultipleOfFive = firstNumerator + (-firstNumerator % 5)
        for numerator in range(firstMultipleOfFive, denominator, 5):
            if (numerator + denominator) & 1 and gcd(numerator, denominator) == 1:
                numeratorSquared = numerator * numerator
                first = (5 * denominatorSquared - numeratorSquared) // 5
                second = (
                    5 * denominatorSquared
                    + numeratorSquared
                    - 5 * numerator * denominator
                ) // 5
                total += limit // (first * second)

    return total


def runTests():
    assert canonicalTriplet(1, 2) == (209, 247, 286)
    assert canonicalTripletCount(10**3) == 7
    assert canonicalTripletCount(10**4) == 106
    assert canonicalTripletCount(10**6) == 11845


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = canonicalTripletCount(10**17)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
