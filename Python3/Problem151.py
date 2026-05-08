import functools
import time
from fractions import Fraction


FINAL_SINGLE_A5 = (0, 0, 0, 1)


def nextState(state, index):
    next_state = list(state)
    next_state[index] -= 1

    for smaller in range(index + 1, len(next_state)):
        next_state[smaller] += 1

    return tuple(next_state)


@functools.lru_cache(maxsize=None)
def expectedSingles(state):
    total_sheets = sum(state)
    if total_sheets == 0:
        return Fraction(0)

    current = Fraction(1) if total_sheets == 1 and state != FINAL_SINGLE_A5 else Fraction(0)
    future = Fraction(0)

    for index, count in enumerate(state):
        if count:
            future += Fraction(count, total_sheets) * expectedSingles(nextState(state, index))

    return current + future


def runTests():
    assert nextState((1, 0, 0, 0), 0) == (0, 1, 1, 1)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = float(expectedSingles((1, 1, 1, 1)))
    elapsed = time.time() - start

    print("Found " + format(answer, ".6f") + " in " + str(elapsed) + " seconds.")
