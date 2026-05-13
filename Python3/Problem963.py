from collections import Counter
from functools import cache
import time


TARGET = 100_000


def ternary(value):
    digits = []
    while value:
        digits.append(str(value % 3))
        value //= 3
    return "".join(reversed(digits)) or "0"


def dyadicTable(limit):
    power = 1
    while power <= limit:
        power *= 3
    size = 1 << (power.bit_length())
    values = [0.0] * (size + 1)

    for index in range(1, size + 1):
        previous = values[index >> 1]
        if index & 1:
            values[index] = previous + 1
        elif previous < 2:
            values[index] = previous / 2
        else:
            values[index] = previous - 1

    return values


def numberSignature(value, dyadicValues):
    digits = ternary(value)
    lastZeroBeforeFirstOne = -1

    for index, digit in enumerate(digits):
        if digit == "1":
            break
        if digit == "0":
            lastZeroBeforeFirstOne = index

    prefixRuns = []
    if lastZeroBeforeFirstOne >= 0:
        zeroRun = 0
        for digit in reversed(digits[:lastZeroBeforeFirstOne]):
            if digit == "0":
                zeroRun += 1
            else:
                prefixRuns.append(zeroRun)

    withoutTwos = "".join(digit for digit in digits if digit != "2")
    dyadic = dyadicValues[int(withoutTwos, 2)] if withoutTwos else 0.0
    twoParity = digits.count("2") & 1
    return (tuple(prefixRuns), twoParity, dyadic)


def combinedPairSignature(left, right):
    return (
        tuple(sorted(left[0] + right[0])),
        left[1] ^ right[1],
        left[2] + right[2],
    )


def F(limit):
    dyadicValues = dyadicTable(limit)
    singleCounts = Counter(
        numberSignature(value, dyadicValues) for value in range(1, limit + 1)
    )
    pairCountsDoubled = Counter()

    for leftSignature, leftCount in singleCounts.items():
        for rightSignature, rightCount in singleCounts.items():
            pairCountsDoubled[combinedPairSignature(leftSignature, rightSignature)] += (
                leftCount * (rightCount + (leftSignature == rightSignature))
            )

    return sum(count * count for count in pairCountsDoubled.values()) // 4


def removeTrit(value, trit):
    if value == 0:
        return set()

    digits = ternary(value)
    moves = set()

    for index, digit in enumerate(digits):
        if digit != trit:
            continue
        reduced = (digits[:index] + digits[index + 1 :]).lstrip("0")
        moves.add(int(reduced, 3) if reduced else 0)

    return moves


@cache
def currentPlayerWins(leftPaper, rightPaper, turn):
    leftPaper = tuple(sorted(leftPaper))
    rightPaper = tuple(sorted(rightPaper))
    moves = []

    ownPaper = leftPaper if turn == 0 else rightPaper
    opponentPaper = rightPaper if turn == 0 else leftPaper

    for paperIndex, paper in enumerate((ownPaper, opponentPaper)):
        for numberIndex, value in enumerate(paper):
            allowedTrits = ("0", "2") if paperIndex == 0 else ("1", "2")
            for trit in allowedTrits:
                for nextValue in removeTrit(value, trit):
                    nextOwn = list(ownPaper)
                    nextOpponent = list(opponentPaper)
                    if paperIndex == 0:
                        nextOwn[numberIndex] = nextValue
                    else:
                        nextOpponent[numberIndex] = nextValue

                    if turn == 0:
                        nextLeft = tuple(sorted(nextOwn))
                        nextRight = tuple(sorted(nextOpponent))
                    else:
                        nextLeft = tuple(sorted(nextOpponent))
                        nextRight = tuple(sorted(nextOwn))
                    moves.append((nextLeft, nextRight))

    if not moves:
        return False

    return any(
        not currentPlayerWins(nextLeft, nextRight, 1 - turn)
        for nextLeft, nextRight in moves
    )


def bruteF(limit):
    pairs = [(left, right) for left in range(1, limit + 1) for right in range(left, limit + 1)]
    total = 0
    for leftPair in pairs:
        for rightPair in pairs:
            if not currentPlayerWins(leftPair, rightPair, 0) and not currentPlayerWins(
                leftPair, rightPair, 1
            ):
                total += 1
    return total


def solve():
    return F(TARGET)


def runTests():
    assert F(5) == 21
    assert bruteF(5) == 21


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
