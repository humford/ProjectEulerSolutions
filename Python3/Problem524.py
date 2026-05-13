import itertools
import math
import time
from functools import cache


def firstSortSteps(items):
    items = list(items)
    steps = 0
    while True:
        for index in range(len(items) - 1):
            if items[index] > items[index + 1]:
                value = items.pop(index + 1)
                items.insert(0, value)
                steps += 1
                break
        else:
            return steps


def lexicographicRank(permutation):
    remaining = list(range(1, len(permutation) + 1))
    rank = 1

    for index, value in enumerate(permutation):
        smallerUnused = remaining.index(value)
        rank += smallerUnused * math.factorial(len(permutation) - index - 1)
        remaining.pop(smallerUnused)

    return rank


def qValues(n):
    result = {}
    for index, permutation in enumerate(itertools.permutations(range(1, n + 1)), start=1):
        steps = firstSortSteps(permutation)
        result.setdefault(steps, index)
    return result


def shiftPermutation(permutation, offset):
    return tuple(value + offset for value in permutation)


def firstConstrainedPermutation(n, steps, increasingPrefixLength=0):
    """First length-n permutation with a fixed first-sort count.

    The optional prefix constraint asks for the first increasingPrefixLength
    positions to be increasing.  A constrained state exists exactly when the
    binary expansion of steps has no more set bits than the unconstrained tail
    length n - increasingPrefixLength.
    """
    return _firstConstrainedPermutation(n, steps, increasingPrefixLength)


@cache
def _firstConstrainedPermutation(n, steps, increasingPrefixLength):
    if (
        n < 1
        or increasingPrefixLength < 0
        or increasingPrefixLength > n
        or steps < 0
        or steps > 2 ** (n - 1) - 1
        or steps.bit_count() > n - increasingPrefixLength
    ):
        return None

    if n == 1:
        return (1,) if steps == 0 else None

    if steps % 2 == 0:
        suffixPrefixLength = increasingPrefixLength - 1 if increasingPrefixLength else 0
        suffix = _firstConstrainedPermutation(n - 1, steps // 2, suffixPrefixLength)
        if suffix is None:
            return None
        return (1,) + shiftPermutation(suffix, 1)

    if increasingPrefixLength <= 1 and steps % 4 == 1:
        if n == 2:
            return (2, 1) if steps == 1 else None

        suffix = _firstConstrainedPermutation(n - 2, (steps - 1) // 4, 0)
        if suffix is not None:
            return (2, 1) + shiftPermutation(suffix, 2)

    best = None
    minLeftSteps = max(0, steps - 1 - 2 * (2 ** (n - 2) - 1))

    for leftLength in range(1, n):
        if increasingPrefixLength and increasingPrefixLength > leftLength:
            continue

        leftPrefixLength = increasingPrefixLength if increasingPrefixLength else 0
        maxLeftSteps = min(2 ** (leftLength - 1) - 1, steps - 1)
        leftSteps = minLeftSteps
        if (leftSteps - (steps - 1)) % 2:
            leftSteps += 1

        while leftSteps <= maxLeftSteps:
            rightSteps = (steps - leftSteps - 1) // 2
            if (
                leftSteps.bit_count() <= leftLength - leftPrefixLength
                and rightSteps.bit_count() <= n - 1 - leftLength
            ):
                left = _firstConstrainedPermutation(
                    leftLength, leftSteps, leftPrefixLength
                )
                right = _firstConstrainedPermutation(n - 1, rightSteps, leftLength)

                if left is not None and right is not None:
                    sortedLeftValues = right[:leftLength]
                    candidate = (
                        tuple(sortedLeftValues[value - 1] + 1 for value in left)
                        + (1,)
                        + shiftPermutation(right[leftLength:], 1)
                    )
                    if best is None or candidate < best:
                        best = candidate

            leftSteps += 2

    return best


def firstSortIndex(steps):
    while steps and steps % 2 == 0:
        steps //= 2

    if steps == 0:
        return 1

    n = 1
    while 2 ** (n - 1) - 1 < steps:
        n += 1

    permutation = firstConstrainedPermutation(n, steps)
    return lexicographicRank(permutation)


def runTests():
    q4 = qValues(4)
    assert q4[0] == 1
    assert q4[4] == 2
    assert q4[2] == 3
    assert q4[6] == 5
    assert q4[1] == 7
    assert q4[5] == 8
    assert q4[3] == 12
    assert q4[7] == 19

    for n in range(1, 8):
        qn = qValues(n)
        for steps in range(2 ** (n - 1)):
            permutation = firstConstrainedPermutation(n, steps)
            assert firstSortSteps(permutation) == steps
            assert lexicographicRank(permutation) == qn[steps]

    assert firstSortIndex(3) == 5
    assert firstSortIndex(9) == 26
    assert firstSortIndex(2 ** 8) == 2
    assert firstSortIndex(12 ** 2) == 26


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstSortIndex(12 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
