import time


TARGET = 16


def g(days):
    """Return the maximal number of blue points after the given number of days.

    A projective normalization sends the three red points to infinity in three
    directions. The generated lines then form three parallel families whose
    parameters are lattice points in a growing hexagonal region. Counting
    pairwise intersections of those line families, with triple intersections
    subtracted, gives this Ehrhart-type closed form.
    """
    sign = -1 if days % 2 else 1
    numerator = (
        11 * (1 << (4 * days))
        + 132 * (1 << (3 * days))
        + 564 * (1 << (2 * days))
        + 1008 * (1 << days)
        - 384 * sign
        - 128 * sign * (1 << days)
        + 768
    )
    assert numerator % 864 == 0
    return numerator // 864


def solve():
    return g(TARGET)


def runTests():
    assert g(1) == 8
    assert g(2) == 28


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
