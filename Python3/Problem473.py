from bisect import bisect_right
from collections import defaultdict
from decimal import Decimal, getcontext
import time


PROBLEM_LIMIT = 10**10


def fibonacciNumbers(count):
    values = [0, 1]
    for _ in range(2, count + 1):
        values.append(values[-1] + values[-2])
    return values


def phigitalPairTerms(limit):
    getcontext().prec = 80
    phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    fib = fibonacciNumbers(200)
    terms = []

    for exponent in range(1, len(fib) - 2):
        if exponent % 2 == 0:
            phiCoefficient = fib[exponent] + fib[exponent + 1]
            integerPart = fib[exponent - 1] - fib[exponent + 2]
        else:
            phiCoefficient = fib[exponent] - fib[exponent + 1]
            integerPart = fib[exponent - 1] + fib[exponent + 2]

        value = Decimal(phiCoefficient) * phi + Decimal(integerPart)
        if value > limit:
            break

        terms.append((exponent, phiCoefficient, integerPart))

    return terms


def subsetStates(terms):
    states = []
    lastPosition = len(terms) - 1

    def search(position, previousChosen, phiCoefficient, integerPart,
               lowBoundary, highBoundary):
        if position == len(terms):
            states.append((phiCoefficient, integerPart, lowBoundary, highBoundary))
            return

        search(
            position + 1, False, phiCoefficient, integerPart,
            lowBoundary, highBoundary
        )

        if not previousChosen:
            _, termPhiCoefficient, termIntegerPart = terms[position]
            search(
                position + 1,
                True,
                phiCoefficient + termPhiCoefficient,
                integerPart + termIntegerPart,
                lowBoundary or position == 0,
                highBoundary or position == lastPosition,
            )

    search(0, False, 0, 0, False, False)
    return states


def indexedRightStates(states):
    groups = defaultdict(lambda: {False: [], True: []})

    for phiCoefficient, integerPart, lowBoundary, _ in states:
        groups[phiCoefficient][lowBoundary].append(integerPart)

    prefixSums = {}
    for phiCoefficient, byBoundary in groups.items():
        prefixSums[phiCoefficient] = {}
        for lowBoundary, values in byBoundary.items():
            values.sort()
            runningTotal = 0
            prefixes = [0]
            for value in values:
                runningTotal += value
                prefixes.append(runningTotal)
            prefixSums[phiCoefficient][lowBoundary] = prefixes

    return groups, prefixSums


def phigitalPalindromeSum(limit):
    terms = phigitalPairTerms(limit)
    split = len(terms) // 2
    leftTerms = terms[:split]
    rightTerms = terms[split:]
    leftStates = subsetStates(leftTerms)
    rightStates = subsetStates(rightTerms)
    rightGroups, rightPrefixSums = indexedRightStates(rightStates)

    total = 1 if limit >= 1 else 0
    touchingBoundary = (
        bool(leftTerms and rightTerms)
        and leftTerms[-1][0] + 1 == rightTerms[0][0]
    )

    for phiCoefficient, integerPart, _, highBoundary in leftStates:
        targetCoefficient = -phiCoefficient
        if targetCoefficient not in rightGroups:
            continue

        maxRightPart = limit - integerPart
        for rightLowBoundary in (False, True):
            if touchingBoundary and highBoundary and rightLowBoundary:
                continue

            rightValues = rightGroups[targetCoefficient][rightLowBoundary]
            count = bisect_right(rightValues, maxRightPart)
            total += (
                count * integerPart
                + rightPrefixSums[targetCoefficient][rightLowBoundary][count]
            )

    return total


def brutePhigitalPalindromeSum(limit):
    terms = phigitalPairTerms(limit)
    total = 1 if limit >= 1 else 0

    def search(position, previousChosen, phiCoefficient, integerPart, usedTerm):
        nonlocal total
        if position == len(terms):
            if usedTerm and phiCoefficient == 0 and integerPart <= limit:
                total += integerPart
            return

        search(position + 1, False, phiCoefficient, integerPart, usedTerm)
        if not previousChosen:
            _, termPhiCoefficient, termIntegerPart = terms[position]
            search(
                position + 1,
                True,
                phiCoefficient + termPhiCoefficient,
                integerPart + termIntegerPart,
                True,
            )

    search(0, False, 0, 0, False)
    return total


def runTests():
    assert phigitalPalindromeSum(1_000) == 4_345
    assert phigitalPalindromeSum(1_000) == brutePhigitalPalindromeSum(1_000)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = phigitalPalindromeSum(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
