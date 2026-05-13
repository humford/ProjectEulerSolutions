from collections import Counter
from fractions import Fraction
from math import comb, factorial
import time


TARGET = 7


def partitions(total, maximum=None):
    if total == 0:
        yield []
        return

    if maximum is None or maximum > total:
        maximum = total

    for first in range(maximum, 0, -1):
        for rest in partitions(total - first, first):
            yield [first] + rest


def zValue(partition):
    counts = Counter(partition)
    value = 1
    for cycleLength, multiplicity in counts.items():
        value *= cycleLength**multiplicity * factorial(multiplicity)
    return value


def multiplyPolynomials(left, right, degreeLimit):
    product = [0] * (min(degreeLimit, len(left) + len(right) - 2) + 1)
    for leftDegree, leftValue in enumerate(left):
        if leftValue == 0:
            continue
        for rightDegree, rightValue in enumerate(right):
            degree = leftDegree + rightDegree
            if rightValue and degree <= degreeLimit:
                product[degree] += leftValue * rightValue
    return product


def hookCharacter(n, hookLegLength, smallCycleType):
    degreeLimit = n - 1
    cycleCounts = Counter(smallCycleType)
    cycleCounts[1] += n - sum(smallCycleType)
    polynomial = [1]

    for cycleLength, multiplicity in cycleCounts.items():
        factor = [0] * (cycleLength + 1)
        factor[0] = 1
        factor[cycleLength] = -((-1) ** cycleLength)
        for _ in range(multiplicity):
            polynomial = multiplyPolynomials(polynomial, factor, degreeLimit)

    quotient = []
    previous = 0
    for degree in range(degreeLimit + 1):
        coefficient = polynomial[degree] if degree < len(polynomial) else 0
        current = coefficient - previous
        quotient.append(current)
        previous = current

    return quotient[hookLegLength]


def roundScalar(n, hookLegLength, selectedCount):
    dimension = comb(n - 1, hookLegLength)
    averageTrace = Fraction(0, 1)

    for cycleType in partitions(selectedCount):
        averageTrace += Fraction(
            hookCharacter(n, hookLegLength, cycleType), zValue(cycleType)
        )

    return averageTrace / dimension


def probability(k):
    children = k * (k - 1) // 2 + 1
    total = Fraction(0, 1)

    for hookLegLength in range(children):
        contribution = Fraction(comb(children - 1, hookLegLength), 1)
        if hookLegLength % 2:
            contribution = -contribution

        for selectedCount in range(1, k + 1):
            contribution *= roundScalar(children, hookLegLength, selectedCount)

        total += contribution

    return total / factorial(children)


def solve():
    return probability(TARGET)


def runTests():
    assert probability(3) == Fraction(1, 72)
    assert format(float(probability(3)), ".10e") == "1.3888888889e-02"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + format(float(answer), ".10e") + " in " + str(elapsed) + " seconds.")
