from array import array
from functools import lru_cache
import time


MODULUS = 1_234_567_891
TARGET = 5_000
INVERSE_TWO = (MODULUS + 1) // 2


def partitionNumbers(limit):
    partitions = [0] * (limit + 1)
    partitions[0] = 1

    for part in range(1, limit + 1):
        for total in range(part, limit + 1):
            partitions[total] = (partitions[total] + partitions[total - part]) % MODULUS

    return partitions


def excessPartitionCounts(limit):
    # A partition with m piles and s stones has excess e = s - m.
    # Subtracting one stone from each pile turns it into a partition of e
    # into at most m parts.
    maxExcess = limit // 2 + 1
    counts = [array("I", [1] * (limit + 1))]

    for excess in range(1, maxExcess + 1):
        row = array("I", [0] * (limit + 1))
        value = 0

        for maxParts in range(1, limit + 1):
            if maxParts <= excess:
                value = (value + counts[excess - maxParts][maxParts]) % MODULUS
            row[maxParts] = value

        counts.append(row)

    return counts


def prefixByParity(row, limit):
    allPrefix = [0] * (limit + 1)
    evenPrefix = [0] * (limit + 1)
    oddPrefix = [0] * (limit + 1)
    allTotal = 0
    evenTotal = 0
    oddTotal = 0

    for index in range(limit + 1):
        value = row[index]
        allTotal = (allTotal + value) % MODULUS

        if index % 2 == 0:
            evenTotal = (evenTotal + value) % MODULUS
        else:
            oddTotal = (oddTotal + value) % MODULUS

        allPrefix[index] = allTotal
        evenPrefix[index] = evenTotal
        oddPrefix[index] = oddTotal

    return allPrefix, evenPrefix, oddPrefix


def E(limit):
    partitions = partitionNumbers(limit)
    partitionPrefix = []
    running = 0
    for value in partitions:
        running = (running + value) % MODULUS
        partitionPrefix.append(running)

    allSettings = sum(
        partitions[aStones] * partitionPrefix[limit - aStones]
        for aStones in range(limit + 1)
    ) % MODULUS

    counts = excessPartitionCounts(limit)
    equalExcess = 0
    oneMoreExcess = 0
    oneMoreExcessOddPiles = 0

    for excess in range(0, limit // 2 + 1):
        remaining = limit - 2 * excess
        row = counts[excess]
        allPrefix, evenPrefix, oddPrefix = prefixByParity(row, remaining)

        for aParts in range(remaining + 1):
            equalExcess = (
                equalExcess
                + row[aParts] * allPrefix[remaining - aParts]
            ) % MODULUS

        if 2 * excess + 1 <= limit:
            remaining = limit - (2 * excess + 1)
            rowA = counts[excess + 1]

            for aParts in range(remaining + 1):
                value = rowA[aParts]
                oneMoreExcess = (
                    oneMoreExcess
                    + value * allPrefix[remaining - aParts]
                ) % MODULUS

                oppositeParityPrefix = (
                    evenPrefix if aParts % 2 else oddPrefix
                )
                oneMoreExcessOddPiles = (
                    oneMoreExcessOddPiles
                    + value * oppositeParityPrefix[remaining - aParts]
                ) % MODULUS

    # Let d = excess(A) - excess(B).  The game is A-always-winning exactly
    # when d >= 2, or when d = 1 and the total number of piles is odd.
    return (
        (allSettings - equalExcess - 2 * oneMoreExcess) * INVERSE_TWO
        + oneMoreExcessOddPiles
    ) % MODULUS


def bruteE(limit):
    def normalize(piles):
        return tuple(sorted((pile for pile in piles if pile > 0), reverse=True))

    def leftMoves(aPiles, bPiles):
        aPiles = list(aPiles)
        bPiles = list(bPiles)
        seen = set()

        for index in range(len(aPiles)):
            state = (normalize(aPiles[:index] + aPiles[index + 1:]), tuple(bPiles))
            if state not in seen:
                seen.add(state)
                yield state

        for index in range(len(bPiles)):
            nextB = bPiles.copy()
            nextB[index] -= 1
            state = (tuple(aPiles), normalize(nextB))
            if state not in seen:
                seen.add(state)
                yield state

    def rightMoves(aPiles, bPiles):
        for nextB, nextA in leftMoves(bPiles, aPiles):
            yield nextA, nextB

    @lru_cache(None)
    def outcome(aPiles, bPiles):
        leftOptions = list(leftMoves(aPiles, bPiles))
        rightOptions = list(rightMoves(aPiles, bPiles))
        leftWinsMovingFirst = (
            any(outcome(*option)[1] for option in leftOptions)
            if leftOptions
            else False
        )
        leftWinsMovingSecond = (
            all(outcome(*option)[0] for option in rightOptions)
            if rightOptions
            else True
        )
        return leftWinsMovingFirst, leftWinsMovingSecond

    def partitions(total, maximum=None):
        if total == 0:
            yield ()
            return
        if maximum is None or maximum > total:
            maximum = total
        for first in range(maximum, 0, -1):
            for rest in partitions(total - first, first):
                yield (first,) + rest

    count = 0
    for total in range(1, limit + 1):
        for aTotal in range(total + 1):
            for aPiles in partitions(aTotal):
                for bPiles in partitions(total - aTotal):
                    if outcome(aPiles, bPiles) == (True, True):
                        count += 1

    return count


def solve():
    return E(TARGET)


def runTests():
    assert E(4) == 9
    assert E(10) == bruteE(10) == 486


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
