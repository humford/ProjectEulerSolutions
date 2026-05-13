from collections import defaultdict
from itertools import product
from math import comb
import time


CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
SUIT_CHOICES = [comb(4, count) for count in range(5)]
PAIR_SCORES = [2 * comb(count, 2) for count in range(5)]


def subsetSumPolynomial(counts, values):
    polynomial = [0] * 16
    polynomial[0] = 1

    for count, value in zip(counts, values):
        nextPolynomial = [0] * 16
        for currentSum, ways in enumerate(polynomial):
            if ways == 0:
                continue

            for chosen in range(count + 1):
                newSum = currentSum + chosen * value
                if newSum <= 15:
                    nextPolynomial[newSum] += ways * comb(count, chosen)

        polynomial = nextPolynomial

    return polynomial


def runScore(counts):
    total = 0
    index = 0

    while index < len(counts):
        if counts[index] == 0:
            index += 1
            continue

        end = index
        productCount = 1
        while end < len(counts) and counts[end] > 0:
            productCount *= counts[end]
            end += 1

        length = end - index
        if length >= 3:
            total += length * productCount

        index = end

    return total


def cribbageScore(counts):
    pairScore = sum(PAIR_SCORES[count] for count in counts)
    fifteenScore = 2 * subsetSumPolynomial(counts, CARD_VALUES)[15]
    return pairScore + runScore(counts) + fifteenScore


def handScore(counts):
    return sum(count * value for count, value in zip(counts, CARD_VALUES))


PREFIX_VALUES = CARD_VALUES[:9]
PREFIX_TRANSITIONS = {
    (value, count): [
        (chosen * value, comb(count, chosen))
        for chosen in range(count + 1)
        if chosen * value <= 15
    ]
    for value in PREFIX_VALUES
    for count in range(5)
}


def updatePrefixPolynomial(polynomial, value, count):
    if count == 0:
        return polynomial

    nextPolynomial = [0] * 16
    for currentSum, ways in enumerate(polynomial):
        if ways == 0:
            continue

        for addedSum, coefficient in PREFIX_TRANSITIONS[(value, count)]:
            newSum = currentSum + addedSum
            if newSum <= 15:
                nextPolynomial[newSum] += ways * coefficient

    return tuple(nextPolynomial)


def prefixRecords():
    records = []
    boundaries = set()

    def search(rankIndex, handTotal, pairTotal, polynomial, multiplicity,
               closedRunScore, trailingLength, trailingProduct):
        if rankIndex == 9:
            base = handTotal - pairTotal - closedRunScore - 2 * polynomial[15]
            records.append((
                base,
                polynomial[5],
                trailingLength,
                trailingProduct,
                multiplicity,
            ))
            boundaries.add((trailingLength, trailingProduct))
            return

        value = PREFIX_VALUES[rankIndex]
        closedAfterZero = closedRunScore
        if trailingLength >= 3:
            closedAfterZero += trailingLength * trailingProduct
        search(
            rankIndex + 1,
            handTotal,
            pairTotal,
            polynomial,
            multiplicity,
            closedAfterZero,
            0,
            1,
        )

        for count in range(1, 5):
            search(
                rankIndex + 1,
                handTotal + count * value,
                pairTotal + PAIR_SCORES[count],
                updatePrefixPolynomial(polynomial, value, count),
                multiplicity * SUIT_CHOICES[count],
                closedRunScore,
                trailingLength + 1,
                trailingProduct * count,
            )

    search(0, 0, 0, (1,) + (0,) * 15, 1, 0, 0, 1)
    return records, boundaries


def suffixSummary(counts):
    totalCards = sum(counts)
    handTotal = 10 * totalCards
    pairTotal = sum(PAIR_SCORES[count] for count in counts)
    multiplicity = 1
    for count in counts:
        multiplicity *= SUIT_CHOICES[count]

    leadingLength = 0
    leadingProduct = 1
    index = 0
    while index < 4 and counts[index] > 0:
        leadingLength += 1
        leadingProduct *= counts[index]
        index += 1

    closedRunScore = 0
    while index < 4:
        if counts[index] == 0:
            index += 1
            continue

        end = index
        productCount = 1
        while end < 4 and counts[end] > 0:
            productCount *= counts[end]
            end += 1

        length = end - index
        if length >= 3:
            closedRunScore += length * productCount
        index = end

    return (
        totalCards,
        pairTotal + closedRunScore - handTotal,
        leadingLength,
        leadingProduct,
        multiplicity,
    )


def boundaryRunScore(leftLength, leftProduct, rightLength, rightProduct):
    if leftLength == 0 and rightLength == 0:
        return 0
    if leftLength == 0:
        return rightLength * rightProduct if rightLength >= 3 else 0
    if rightLength == 0:
        return leftLength * leftProduct if leftLength >= 3 else 0

    length = leftLength + rightLength
    return length * leftProduct * rightProduct if length >= 3 else 0


def matchingHandCount():
    records, boundaries = prefixRecords()
    suffixesByCardCount = [[] for _ in range(17)]

    for counts in product(range(5), repeat=4):
        suffixesByCardCount[sum(counts)].append(suffixSummary(counts))

    answer = 0
    for totalTens in range(17):
        index = defaultdict(int)
        for base, fiveWays, trailLength, trailProduct, multiplicity in records:
            key = (base - 2 * totalTens * fiveWays, trailLength, trailProduct)
            index[key] += multiplicity

        for _, suffixConstant, leadLength, leadProduct, suffixMultiplicity in (
            suffixesByCardCount[totalTens]
        ):
            matchingPrefixes = 0
            for trailLength, trailProduct in boundaries:
                required = suffixConstant + boundaryRunScore(
                    trailLength,
                    trailProduct,
                    leadLength,
                    leadProduct,
                )
                matchingPrefixes += index.get(
                    (required, trailLength, trailProduct),
                    0,
                )

            answer += matchingPrefixes * suffixMultiplicity

    return answer - 1


def solve():
    return matchingHandCount()


def runTests():
    counts = [0] * 13
    counts[4] = 3
    counts[12] = 1
    assert cribbageScore(counts) == 14

    counts = [0] * 13
    counts[0] = 2
    counts[1] = counts[2] = counts[3] = counts[4] = 1
    assert handScore(counts) == 16
    assert cribbageScore(counts) == 16


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
