import time
from collections import defaultdict


TARGET = 30
SIDES = 6
WIN_THRESHOLD = SIDES * SIDES // 2
SCORE_CAP = WIN_THRESHOLD + 1


def secondBeatsFirst(first, second):
    return sum(1 for firstRoll in first for secondRoll in second if secondRoll > firstRoll) > WIN_THRESHOLD


def choiceTriples(remainingA, remainingB, remainingC):
    choices = []

    for countA in range(remainingA + 1):
        for countB in range(remainingB + 1):
            for countC in range(remainingC + 1):
                choices.append((countA, countB, countC))

    return choices


def nontransitiveSets(maxPip=TARGET):
    states = {(0, 0, 0, 0, 0, 0): 1}
    choicesCache = {}

    for _ in range(1, maxPip + 1):
        nextStates = defaultdict(int)

        for (usedA, usedB, usedC, bBeatsA, cBeatsB, aBeatsC), ways in states.items():
            remaining = (SIDES - usedA, SIDES - usedB, SIDES - usedC)
            if remaining not in choicesCache:
                choicesCache[remaining] = choiceTriples(*remaining)

            for countA, countB, countC in choicesCache[remaining]:
                nextStates[
                    (
                        usedA + countA,
                        usedB + countB,
                        usedC + countC,
                        min(SCORE_CAP, bBeatsA + countB * usedA),
                        min(SCORE_CAP, cBeatsB + countC * usedB),
                        min(SCORE_CAP, aBeatsC + countA * usedC),
                    )
                ] += ways

        states = nextStates

    orientedCycles = states.get((SIDES, SIDES, SIDES, SCORE_CAP, SCORE_CAP, SCORE_CAP), 0)
    return orientedCycles // 3


def runTests():
    dieA = (1, 4, 4, 4, 4, 4)
    dieB = (2, 2, 2, 5, 5, 5)
    dieC = (3, 3, 3, 3, 3, 6)

    assert secondBeatsFirst(dieA, dieB)
    assert secondBeatsFirst(dieB, dieC)
    assert secondBeatsFirst(dieC, dieA)
    assert nontransitiveSets(7) == 9780


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nontransitiveSets()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
