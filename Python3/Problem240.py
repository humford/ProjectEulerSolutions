from collections import defaultdict
from math import comb
import time


def topDiceRolls(dice, sides, top_dice, target):
    states = {(0, 0, 0): 1}

    for face in range(sides, 0, -1):
        next_states = defaultdict(int)

        for (assigned, taken, total), ways in states.items():
            remaining = dice - assigned

            for count in range(remaining + 1):
                newly_taken = min(count, top_dice - taken)
                next_total = total + face * newly_taken

                if next_total <= target:
                    next_states[
                        (
                            assigned + count,
                            taken + newly_taken,
                            next_total,
                        )
                    ] += ways * comb(remaining, count)

        states = next_states

    return states[(dice, top_dice, target)]


def runTests():
    assert topDiceRolls(5, 6, 3, 15) == 1111


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = topDiceRolls(20, 12, 10, 70)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
