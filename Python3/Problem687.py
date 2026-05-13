import time
from decimal import Decimal, ROUND_HALF_UP, getcontext
from math import comb, factorial, gcd


RANK_COUNT = 13
COPIES_PER_RANK = 4
CARD_COUNT = RANK_COUNT * COPIES_PER_RANK


def multiplyPolynomials(first, second):
    result = [0] * (len(first) + len(second) - 1)
    for i, firstCoefficient in enumerate(first):
        if firstCoefficient == 0:
            continue
        for j, secondCoefficient in enumerate(second):
            if secondCoefficient:
                result[i + j] += firstCoefficient * secondCoefficient
    return result


def exactPerfectRankDistribution():
    scaledInclusionPolynomial = [1, -12, 36, -24]
    scaling = factorial(COPIES_PER_RANK) ** RANK_COUNT

    factorials = [1] * (CARD_COUNT + 1)
    for i in range(2, CARD_COUNT + 1):
        factorials[i] = factorials[i - 1] * i

    powers = [[1]]
    for _ in range(RANK_COUNT):
        powers.append(multiplyPolynomials(powers[-1], scaledInclusionPolynomial))

    fixedPerfectCounts = [0] * (RANK_COUNT + 1)
    for constrainedRanks in range(RANK_COUNT + 1):
        numerator = 0
        for gluedGaps, coefficient in enumerate(powers[constrainedRanks]):
            numerator += factorials[CARD_COUNT - gluedGaps] * coefficient
        assert numerator % scaling == 0
        fixedPerfectCounts[constrainedRanks] = numerator // scaling

    fixedSubsetExactCounts = [0] * (RANK_COUNT + 1)
    for perfectRanks in range(RANK_COUNT + 1):
        total = 0
        for constrainedRanks in range(perfectRanks, RANK_COUNT + 1):
            term = (
                comb(RANK_COUNT - perfectRanks, constrainedRanks - perfectRanks)
                * fixedPerfectCounts[constrainedRanks]
            )
            total = total - term if (constrainedRanks - perfectRanks) & 1 else total + term
        fixedSubsetExactCounts[perfectRanks] = total

    return [
        comb(RANK_COUNT, perfectRanks) * fixedSubsetExactCounts[perfectRanks]
        for perfectRanks in range(RANK_COUNT + 1)
    ]


def primePerfectRankProbability():
    distribution = exactPerfectRankDistribution()
    total = sum(distribution)

    expectedNumerator = sum(
        perfectRanks * distribution[perfectRanks]
        for perfectRanks in range(RANK_COUNT + 1)
    )
    expectedDenominator = total
    divisor = gcd(expectedNumerator, expectedDenominator)
    assert (
        expectedNumerator // divisor,
        expectedDenominator // divisor,
    ) == (4324, 425)

    primeCounts = {2, 3, 5, 7, 11, 13}
    favourable = sum(distribution[count] for count in primeCounts)

    getcontext().prec = 60
    probability = (Decimal(favourable) / Decimal(total)).quantize(
        Decimal("0.0000000000"),
        rounding=ROUND_HALF_UP,
    )
    return format(probability, "f")


def runTests():
    assert primePerfectRankProbability() == "0.3285320869"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primePerfectRankProbability()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
