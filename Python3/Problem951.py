from collections import defaultdict
from itertools import product
import time


TARGET = 26


def fairProbabilityCount(redCards):
    scale = 1 << (2 * redCards)
    half = scale // 2
    states = {(None, 0, 0, 0, 0): 1}

    for _ in range(2 * redCards):
        nextStates = defaultdict(int)

        for (firstColour, topWin, nextWin, red, black), count in states.items():
            if red < redCards:
                if firstColour is None or firstColour != 0:
                    newTopWin = scale - topWin
                else:
                    newTopWin = scale - ((topWin + nextWin) >> 1)
                nextStates[(0, newTopWin, topWin, red + 1, black)] += count

            if black < redCards:
                if firstColour is None or firstColour != 1:
                    newTopWin = scale - topWin
                else:
                    newTopWin = scale - ((topWin + nextWin) >> 1)
                nextStates[(1, newTopWin, topWin, red, black + 1)] += count

        states = nextStates

    return sum(count for (_, topWin, _, _, _), count in states.items() if topWin == half)


def wordWinProbability(word):
    scale = 1 << len(word)
    nextNextWin = 0
    nextWin = 0

    for index in range(len(word) - 1, -1, -1):
        if index + 1 == len(word) or word[index] != word[index + 1]:
            currentWin = scale - nextWin
        else:
            currentWin = scale - ((nextWin + nextNextWin) >> 1)
        nextNextWin = nextWin
        nextWin = currentWin

    return nextWin


def bruteF(redCards):
    scale = 1 << (2 * redCards)
    half = scale // 2
    total = 0

    for word in product((0, 1), repeat=2 * redCards):
        if sum(word) == redCards and wordWinProbability(word) == half:
            total += 1

    return total


def F(redCards):
    return fairProbabilityCount(redCards)


def solve():
    return F(TARGET)


def runTests():
    assert F(2) == 4
    assert F(8) == 11_892
    for redCards in range(1, 7):
        assert F(redCards) == bruteF(redCards)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
