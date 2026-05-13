import math
import time
from collections import defaultdict


RANKS = 13
SUITS = 4
FULL_SUIT_MASK = (1 << SUITS) - 1


def handsWithoutBadugi(maxCards=RANKS):
    # State bit m means that some selection of processed ranks can occupy suit mask m.
    startState = 1
    dp = {(0, startState): 1}
    rankChoices = [0] + list(range(1, 1 << SUITS))

    for _ in range(RANKS):
        nextDp = defaultdict(int)

        for (cards, state), count in dp.items():
            for suitSubset in rankChoices:
                newState = state

                if suitSubset:
                    for mask in range(1 << SUITS):
                        if not (state >> mask) & 1:
                            continue

                        available = suitSubset & ~mask

                        while available:
                            suit = available & -available
                            newState |= 1 << (mask | suit)
                            available -= suit

                if (newState >> FULL_SUIT_MASK) & 1:
                    continue

                nextDp[(cards + suitSubset.bit_count(), newState)] += count

        dp = nextDp

    noBadugi = [0] * (maxCards + 1)

    for (cards, _), count in dp.items():
        if cards <= maxCards:
            noBadugi[cards] += count

    return noBadugi


def badugiHands(cards):
    noBadugi = handsWithoutBadugi(cards)
    return math.comb(52, cards) - noBadugi[cards]


def badugiHandSum():
    noBadugi = handsWithoutBadugi(RANKS)
    return sum(math.comb(52, cards) - noBadugi[cards] for cards in range(4, RANKS + 1))


def runTests():
    assert badugiHands(5) == 514800


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = badugiHandSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
