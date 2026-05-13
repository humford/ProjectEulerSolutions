from itertools import permutations
from math import factorial
import time


def validPermutationCount(counts):
    digits = sum(counts)
    denominator = 1
    for count in counts:
        denominator *= factorial(count)

    total = factorial(digits) // denominator

    if counts[0] == 0:
        return total

    leadingZeroDenominator = factorial(counts[0] - 1)
    for count in counts[1:]:
        leadingZeroDenominator *= factorial(count)

    return total - factorial(digits - 1) // leadingZeroDenominator


def digitCountVectors(totalDigits, digit=0, remaining=None, prefix=None):
    if remaining is None:
        remaining = totalDigits
    if prefix is None:
        prefix = []

    if digit == 9:
        yield prefix + [remaining]
        return

    for count in range(remaining + 1):
        yield from digitCountVectors(
            totalDigits,
            digit + 1,
            remaining - count,
            prefix + [count],
        )


def S(k):
    total = 0

    for counts in digitCountVectors(k):
        if counts[0] == k:
            continue

        permutationsForCounts = validPermutationCount(counts)
        total += permutationsForCounts * (permutationsForCounts - 1) // 2

    return total


def TBruteForce(n):
    digits = str(n)
    values = {
        int("".join(p))
        for p in permutations(digits)
        if p[0] != "0"
    }
    return sum(value > n for value in values)


def runTests():
    assert TBruteForce(2302) == 4
    assert S(3) == 1701


def solve():
    return S(12)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
