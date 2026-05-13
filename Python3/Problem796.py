import math
import time
from decimal import Decimal, ROUND_HALF_UP, getcontext


getcontext().prec = 80
SUM_RATIO_CACHE = {}


def sumChooseRatios(allowedCards, totalCards):
    key = (allowedCards, totalCards)
    cached = SUM_RATIO_CACHE.get(key)
    if cached is not None:
        return cached

    ratio = Decimal(1)
    total = Decimal(1)
    for k in range(1, min(totalCards - 1, allowedCards) + 1):
        ratio *= Decimal(allowedCards - k + 1) / Decimal(totalCards - k + 1)
        total += ratio

    SUM_RATIO_CACHE[key] = total
    return total


def expectationFromCoefficients(totalCards, coefficients):
    total = Decimal(0)
    for allowedCards, coefficient in coefficients.items():
        if coefficient:
            total += Decimal(coefficient) * sumChooseRatios(allowedCards, totalCards)
    return total


def expectedAllRanksSingleDeck():
    totalCards = 54
    coefficients = {}

    for missingRanks in range(1, 14):
        coefficient = (-1) ** (missingRanks + 1) * math.comb(13, missingRanks)
        allowedCards = totalCards - 4 * missingRanks
        coefficients[allowedCards] = coefficients.get(allowedCards, 0) + coefficient

    return expectationFromCoefficients(totalCards, coefficients)


def expectedAllSuitsRanksDecks():
    totalCards = 540
    coefficients = {}

    for missingSuits in range(5):
        suitChoices = math.comb(4, missingSuits)
        for missingRanks in range(14):
            rankChoices = math.comb(13, missingRanks)
            for missingDecks in range(11):
                if missingSuits == missingRanks == missingDecks == 0:
                    continue

                deckChoices = math.comb(10, missingDecks)
                sign = -1 if (missingSuits + missingRanks + missingDecks) % 2 == 0 else 1
                coefficient = sign * suitChoices * rankChoices * deckChoices

                remainingDecks = 10 - missingDecks
                allowedCards = (4 - missingSuits) * (13 - missingRanks) * remainingDecks + 2 * remainingDecks
                coefficients[allowedCards] = coefficients.get(allowedCards, 0) + coefficient

    return expectationFromCoefficients(totalCards, coefficients)


def round8(value):
    return value.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)


def runTests():
    assert round8(expectedAllRanksSingleDeck()) == Decimal("29.05361725")


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = round8(expectedAllSuitsRanksDecks())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
