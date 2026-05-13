from array import array
from bisect import bisect_left
import time


TARGET_PROBABILITIES = list(range(25, 76))


def buildVariables(probabilities):
    counts = [0] * 101
    for probability in probabilities:
        counts[probability] += 1

    variables = []

    for probability in range(50):
        pairs = min(counts[probability], counts[100 - probability])
        if pairs == 0:
            continue

        counts[probability] -= pairs
        counts[100 - probability] -= pairs

        truthful = 100 - probability
        lying = probability
        plusNumerator = truthful * truthful
        plusDenominator = lying * lying
        minusNumerator = lying * lying
        minusDenominator = truthful * truthful

        plusHeads = plusNumerator / 10000.0
        zero = 2 * truthful * lying / 10000.0
        minusHeads = minusNumerator / 10000.0

        for _ in range(pairs):
            variables.append(
                [
                    (minusNumerator, minusDenominator, minusHeads, plusHeads),
                    (1, 1, zero, zero),
                    (plusNumerator, plusDenominator, plusHeads, minusHeads),
                ]
            )

    counts[50] = 0

    for probability in range(101):
        for _ in range(counts[probability]):
            if probability in (0, 100):
                raise ValueError("degenerate probabilities are not supported")
            truthful = 100 - probability
            lying = probability
            variables.append(
                [
                    (lying, truthful, lying / 100.0, truthful / 100.0),
                    (truthful, lying, truthful / 100.0, lying / 100.0),
                ]
            )

    return variables


def enumerateHalf(variables):
    bound = 1
    for variable in variables:
        maximum = 1
        for numerator, denominator, _, _ in variable:
            maximum = max(maximum, numerator, denominator)
        bound *= maximum

    numerators = [1]
    denominators = [1]
    heads = array("d", [1.0])
    tails = array("d", [1.0])

    for variable in variables:
        nextNumerators = []
        nextDenominators = []
        nextHeads = array("d")
        nextTails = array("d")

        for index in range(len(numerators)):
            numerator = numerators[index]
            denominator = denominators[index]
            headProbability = heads[index]
            tailProbability = tails[index]
            for mulNumerator, mulDenominator, headMul, tailMul in variable:
                nextNumerators.append(numerator * mulNumerator)
                nextDenominators.append(denominator * mulDenominator)
                nextHeads.append(headProbability * headMul)
                nextTails.append(tailProbability * tailMul)

        numerators = nextNumerators
        denominators = nextDenominators
        heads = nextHeads
        tails = nextTails

    return numerators, denominators, heads, tails, bound


def fixedPointKeys(numerators, denominators, shift):
    return [
        (numerator << shift) // denominator
        for numerator, denominator in zip(numerators, denominators)
    ]


def sortByKey(keys, heads, tails):
    order = list(range(len(keys)))
    order.sort(key=keys.__getitem__)

    sortedKeys = [0] * len(keys)
    sortedHeads = array("d", [0.0]) * len(keys)
    sortedTails = array("d", [0.0]) * len(keys)

    for outputIndex, inputIndex in enumerate(order):
        sortedKeys[outputIndex] = keys[inputIndex]
        sortedHeads[outputIndex] = heads[inputIndex]
        sortedTails[outputIndex] = tails[inputIndex]

    return sortedKeys, sortedHeads, sortedTails


def suffixSums(values):
    suffix = array("d", [0.0]) * (len(values) + 1)
    total = 0.0

    for index in range(len(values) - 1, -1, -1):
        total += values[index]
        suffix[index] = total

    return suffix


def kahanAdd(total, compensation, value):
    y = value - compensation
    nextTotal = total + y
    return nextTotal, (nextTotal - total) - y


def optimalSuccessProbability(probabilities):
    variables = buildVariables(probabilities)
    if not variables:
        return 0.5

    middle = len(variables) // 2
    left = variables[:middle]
    right = variables[middle:]

    leftNumerators, leftDenominators, leftHeads, leftTails, leftBound = enumerateHalf(left)
    rightNumerators, rightDenominators, rightHeads, rightTails, rightBound = enumerateHalf(right)

    shift = 2 * max(leftBound, rightBound).bit_length() + 4
    rightKeys = fixedPointKeys(rightNumerators, rightDenominators, shift)
    rightKeys, rightHeads, rightTails = sortByKey(rightKeys, rightHeads, rightTails)
    rightSuffixHeads = suffixSums(rightHeads)
    rightSuffixTails = suffixSums(rightTails)

    headsAdvantage = 0.0
    tailsAdvantage = 0.0
    headsCompensation = 0.0
    tailsCompensation = 0.0

    for numerator, denominator, heads, tails in zip(
        leftNumerators,
        leftDenominators,
        leftHeads,
        leftTails,
    ):
        threshold = (denominator << shift) // numerator
        index = bisect_left(rightKeys, threshold)
        headsAdvantage, headsCompensation = kahanAdd(
            headsAdvantage,
            headsCompensation,
            heads * rightSuffixHeads[index],
        )
        tailsAdvantage, tailsCompensation = kahanAdd(
            tailsAdvantage,
            tailsCompensation,
            tails * rightSuffixTails[index],
        )

    totalVariation = max(-1.0, min(1.0, headsAdvantage - tailsAdvantage))
    return (1 + totalVariation) / 2


def solve():
    return f"{optimalSuccessProbability(TARGET_PROBABILITIES):.10f}"


def runTests():
    assert round(optimalSuccessProbability([20, 40, 60, 80]), 3) == 0.832
    assert solve() == "0.9861343531"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
