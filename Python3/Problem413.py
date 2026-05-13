import time
from collections import defaultdict
from functools import lru_cache


def isOneChild(number):
    digits = str(number)
    length = len(digits)
    divisible = 0

    for start in range(length):
        remainder = 0

        for end in range(start, length):
            remainder = (10 * remainder + int(digits[end])) % length

            if remainder == 0:
                divisible += 1

                if divisible > 1:
                    return False

    return divisible == 1


def bruteF(limit):
    return sum(1 for number in range(1, limit) if isOneChild(number))


@lru_cache(maxsize=None)
def oneChildCountWithDigits(length):
    transitions = [
        [(10 * remainder + digit) % length for remainder in range(length)]
        for digit in range(10)
    ]
    states = {((0,) * length, 0): 1}

    for position in range(length):
        nextStates = defaultdict(int)
        digits = range(1, 10) if position == 0 else range(10)

        for (suffixCounts, divisibleCount), ways in states.items():
            for digit in digits:
                nextSuffixCounts = [0] * length
                newDivisible = 0
                transition = transitions[digit]

                for remainder, count in enumerate(suffixCounts):
                    if count == 0:
                        continue

                    nextRemainder = transition[remainder]
                    nextSuffixCounts[nextRemainder] = min(
                        2,
                        nextSuffixCounts[nextRemainder] + count,
                    )

                    if nextRemainder == 0:
                        newDivisible += count

                nextRemainder = digit % length
                nextSuffixCounts[nextRemainder] = min(
                    2,
                    nextSuffixCounts[nextRemainder] + 1,
                )

                if nextRemainder == 0:
                    newDivisible += 1

                totalDivisible = divisibleCount + newDivisible
                if totalDivisible <= 1:
                    nextStates[(tuple(nextSuffixCounts), totalDivisible)] += ways

        states = nextStates

    return sum(
        ways
        for (_, divisibleCount), ways in states.items()
        if divisibleCount == 1
    )


def oneChildCount(limit):
    digits = str(limit)
    if digits[0] != "1" or set(digits[1:]) != {"0"}:
        raise ValueError("oneChildCount expects a power of 10")

    return sum(oneChildCountWithDigits(length) for length in range(1, len(digits)))


def runTests():
    assert isOneChild(5671)
    assert isOneChild(104)
    assert isOneChild(1132451)
    assert bruteF(10) == 9
    assert bruteF(10**3) == 389
    assert oneChildCount(10) == 9
    assert oneChildCount(10**3) == 389
    assert oneChildCount(10**7) == 277674


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = oneChildCount(10**19)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
