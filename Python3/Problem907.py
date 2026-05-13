from functools import lru_cache
import time


MODULUS = 1_000_000_007
TARGET_N = 10_000_000

UP = 0
DOWN = 1

INITIAL_VALUES = [
    2,
    2,
    6,
    12,
    16,
    22,
    36,
    58,
    82,
]

RECURRENCE = [2, -3, 5, -4, 4, -3, 1, -1]


def canPlaceAbove(lower, upper):
    lowerSize, lowerOrientation = lower
    upperSize, upperOrientation = upper

    if lowerOrientation == UP and upperOrientation == UP:
        return upperSize == lowerSize - 1
    if lowerOrientation == DOWN and upperOrientation == DOWN:
        return upperSize == lowerSize + 1
    if lowerOrientation != upperOrientation:
        return abs(upperSize - lowerSize) == 2

    return False


def exhaustiveCount(n):
    cups = [
        (size, orientation)
        for size in range(1, n + 1)
        for orientation in (UP, DOWN)
    ]
    adjacency = [[] for _ in cups]

    for lowerIndex, lower in enumerate(cups):
        for upperIndex, upper in enumerate(cups):
            if lower[0] != upper[0] and canPlaceAbove(lower, upper):
                adjacency[lowerIndex].append(upperIndex)

    fullMask = (1 << n) - 1

    @lru_cache(maxsize=None)
    def countFrom(mask, lastIndex):
        if mask == fullMask:
            return 1

        total = 0
        for nextIndex in adjacency[lastIndex]:
            size = cups[nextIndex][0]
            bit = 1 << (size - 1)
            if not mask & bit:
                total += countFrom(mask | bit, nextIndex)

        return total

    return sum(
        countFrom(1 << (cup[0] - 1), index)
        for index, cup in enumerate(cups)
    )


def combinePolynomials(left, right):
    combined = [0] * (2 * len(RECURRENCE) - 1)

    for leftIndex, leftValue in enumerate(left):
        for rightIndex, rightValue in enumerate(right):
            combined[leftIndex + rightIndex] = (
                combined[leftIndex + rightIndex] + leftValue * rightValue
            ) % MODULUS

    for degree in range(len(combined) - 1, len(RECURRENCE) - 1, -1):
        value = combined[degree]
        if value == 0:
            continue

        for index, coefficient in enumerate(RECURRENCE):
            combined[degree - 1 - index] = (
                combined[degree - 1 - index] + value * coefficient
            ) % MODULUS

    return combined[: len(RECURRENCE)]


def recurrenceValue(n):
    if n <= len(INITIAL_VALUES):
        return INITIAL_VALUES[n - 1] % MODULUS

    state = INITIAL_VALUES[1:9]
    exponent = n - 2
    polynomial = [1] + [0] * (len(RECURRENCE) - 1)
    power = [0, 1] + [0] * (len(RECURRENCE) - 2)

    while exponent:
        if exponent & 1:
            polynomial = combinePolynomials(polynomial, power)
        power = combinePolynomials(power, power)
        exponent //= 2

    return sum(
        coefficient * value
        for coefficient, value in zip(polynomial, state)
    ) % MODULUS


def solve():
    return recurrenceValue(TARGET_N)


def runTests():
    assert exhaustiveCount(4) == 12
    assert exhaustiveCount(8) == 58
    assert exhaustiveCount(20) == 5560

    for n in range(1, 21):
        assert recurrenceValue(n) == exhaustiveCount(n)

    assert solve() == 196_808_901


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
