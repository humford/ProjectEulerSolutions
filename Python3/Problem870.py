from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction
import time


TARGET_INDEX = 123_456
SEQUENCE_TERMS = 10_000


def losingSequence(r, count):
    if r < 1:
        return [1]

    numerator = r.numerator
    denominator = r.denominator
    sequence = [1]
    pointer = 0

    while len(sequence) < count:
        current = sequence[-1]
        while numerator * sequence[pointer] < denominator * current:
            pointer += 1
        sequence.append(current + sequence[pointer])

    return sequence


def losingSequenceForPair(numerator, denominator, count):
    sequence = [1]
    pointer = 0

    while len(sequence) < count:
        current = sequence[-1]
        while numerator * sequence[pointer] < denominator * current:
            pointer += 1
        sequence.append(current + sequence[pointer])

    return sequence


def nextTransition(numerator, denominator, terms=SEQUENCE_TERMS):
    sequence = losingSequenceForPair(numerator, denominator, terms)
    numeratorIndex = 0
    bestNumerator = 0
    bestDenominator = 1

    for denominatorValue in sequence:
        while (
            numeratorIndex < len(sequence)
            and sequence[numeratorIndex] * denominator <= numerator * denominatorValue
        ):
            numeratorIndex += 1

        if numeratorIndex >= len(sequence):
            break

        numeratorValue = sequence[numeratorIndex]
        if (
            bestNumerator == 0
            or numeratorValue * bestDenominator < bestNumerator * denominatorValue
        ):
            bestNumerator = numeratorValue
            bestDenominator = denominatorValue

    return bestNumerator, bestDenominator


def transitionValue(index, terms=SEQUENCE_TERMS):
    numerator = 1
    denominator = 1

    for _ in range(2, index + 1):
        numerator, denominator = nextTransition(numerator, denominator, terms)

    return numerator, denominator


def formatTransition(numerator, denominator, places=10):
    getcontext().prec = 40
    quant = Decimal(1).scaleb(-places)
    value = (Decimal(numerator) / Decimal(denominator)).quantize(
        quant,
        rounding=ROUND_HALF_UP,
    )
    return format(value, "f")


def runTests():
    assert losingSequence(Fraction(1, 2), 10) == [1]
    assert losingSequence(Fraction(1, 1), 6) == [1, 2, 4, 8, 16, 32]
    assert losingSequence(Fraction(2, 1), 7) == [1, 2, 3, 5, 8, 13, 21]
    assert transitionValue(1, 100) == (1, 1)
    assert transitionValue(2, 100) == (2, 1)
    assert transitionValue(22, 100) == (145, 23)
    assert formatTransition(145, 23) == "6.3043478261"


def solve():
    numerator, denominator = transitionValue(TARGET_INDEX)
    return formatTransition(numerator, denominator)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
