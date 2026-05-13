from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction
import time


def firstTwoPairProbability():
    return Fraction(3, 51)


def expectedCardsDrawn():
    initial = (0, 0, 0, 1, 12, 3)
    states = {initial: Fraction(1, 1)}
    survival = [Fraction(0, 1)] * 52
    survival[1] = Fraction(1, 1)

    for drawn in range(1, 51):
        remainingCards = 52 - drawn
        nextStates = {}

        for state, probability in states.items():
            counts = list(state[:5])
            lastRemaining = state[5]

            for remainingOfRank in (1, 2, 3, 4):
                eligibleRanks = counts[remainingOfRank]
                if remainingOfRank == lastRemaining:
                    eligibleRanks -= 1
                if eligibleRanks <= 0:
                    continue

                drawProbability = Fraction(eligibleRanks * remainingOfRank, remainingCards)
                updated = counts[:]
                updated[remainingOfRank] -= 1
                updated[remainingOfRank - 1] += 1
                nextState = tuple(updated + [remainingOfRank - 1])
                nextStates[nextState] = nextStates.get(nextState, Fraction(0, 1)) + probability * drawProbability

        states = nextStates
        survival[drawn + 1] = sum(states.values(), Fraction(0, 1))

    return Fraction(1, 1) + sum(survival[1:52], Fraction(0, 1))


def rounded(value, places=8):
    getcontext().prec = 80
    decimalValue = Decimal(value.numerator) / Decimal(value.denominator)
    quantum = Decimal("0." + "0" * (places - 1) + "1")
    return str(decimalValue.quantize(quantum, rounding=ROUND_HALF_UP))


def runTests():
    assert firstTwoPairProbability() == Fraction(1, 17)
    answer = expectedCardsDrawn()
    assert Fraction(2, 1) <= answer <= Fraction(52, 1)


def solve():
    return rounded(expectedCardsDrawn(), 8)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
