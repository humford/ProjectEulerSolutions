import time
from collections import Counter, deque
from functools import lru_cache


QUINTINOMIAL = sum(1 << exponent for exponent in range(5))


def multiplyModTwo(left, right):
    product = 0
    shift = 0
    while right:
        if right & 1:
            product ^= left << shift
        right >>= 1
        shift += 1

    return product


def splitEvenOddExponents(polynomial):
    evenPart = 0
    oddPart = 0
    exponent = 0
    while polynomial:
        if polynomial & 1:
            if exponent & 1:
                oddPart |= 1 << (exponent // 2)
            else:
                evenPart |= 1 << (exponent // 2)
        polynomial >>= 1
        exponent += 1

    return evenPart, oddPart


def buildAutomaton():
    states = [1]
    stateIndex = {1: 0}
    queue = deque([1])

    while queue:
        polynomial = queue.popleft()
        for digit in [0, 1]:
            source = (
                multiplyModTwo(polynomial, QUINTINOMIAL)
                if digit
                else polynomial
            )
            for part in splitEvenOddExponents(source):
                if part not in stateIndex:
                    stateIndex[part] = len(states)
                    states.append(part)
                    queue.append(part)

    transitions = {}
    for polynomial, index in stateIndex.items():
        for digit in [0, 1]:
            source = (
                multiplyModTwo(polynomial, QUINTINOMIAL)
                if digit
                else polynomial
            )
            counts = Counter(
                stateIndex[part]
                for part in splitEvenOddExponents(source)
            )
            transitions[(index, digit)] = tuple(counts.items())

    baseWeights = tuple(polynomial.bit_count() for polynomial in states)
    return stateIndex[1], transitions, baseWeights


START_STATE, TRANSITIONS, BASE_WEIGHTS = buildAutomaton()


@lru_cache(maxsize=None)
def automatonValues(exponent):
    if exponent == 0:
        return BASE_WEIGHTS

    lowerValues = automatonValues(exponent // 2)
    digit = exponent % 2
    values = []
    for index in range(len(BASE_WEIGHTS)):
        values.append(
            sum(
                coefficient * lowerValues[targetIndex]
                for targetIndex, coefficient in TRANSITIONS[(index, digit)]
            )
        )

    return tuple(values)


def oddQuintinomialCoefficients(exponent):
    return automatonValues(exponent)[START_STATE]


def bruteOddQuintinomialCoefficients(exponent):
    coefficients = {0}
    for _ in range(exponent):
        nextCoefficients = set()
        for currentExponent in coefficients:
            for shift in range(5):
                value = currentExponent + shift
                if value in nextCoefficients:
                    nextCoefficients.remove(value)
                else:
                    nextCoefficients.add(value)
        coefficients = nextCoefficients

    return len(coefficients)


def oddQuintinomialSum():
    return sum(
        oddQuintinomialCoefficients(10 ** exponent)
        for exponent in range(1, 19)
    )


def runTests():
    for exponent in range(12):
        assert (
            oddQuintinomialCoefficients(exponent)
            == bruteOddQuintinomialCoefficients(exponent)
        )

    assert oddQuintinomialCoefficients(3) == 7
    assert oddQuintinomialCoefficients(10) == 17
    assert oddQuintinomialCoefficients(100) == 35


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = oddQuintinomialSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
