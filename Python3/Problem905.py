from functools import lru_cache
import time


TARGET_A_LIMIT = 7
TARGET_B_LIMIT = 19


def nextTurnAfter(turn, player):
    target = player + 1
    if target <= turn:
        target += 3 * ((turn - target) // 3 + 1)
    return target


def applyAlternatingTurns(turn, firstPlayer, secondPlayer, count):
    if count <= 0:
        return turn

    turn = nextTurnAfter(turn, firstPlayer)
    if count == 1:
        return turn

    turn = nextTurnAfter(turn, secondPlayer)
    remaining = count - 2
    turn += 3 * (remaining // 2)

    if remaining % 2:
        turn = nextTurnAfter(turn, firstPlayer)

    return turn


def reductionChunks(numbers):
    values = list(numbers)
    chunks = []

    while True:
        largest = max(range(3), key=lambda index: values[index])
        first, second = [index for index in range(3) if index != largest]

        if values[first] >= values[second]:
            bigger, smaller = first, second
        else:
            bigger, smaller = second, first

        biggerValue = values[bigger]
        smallerValue = values[smaller]

        if biggerValue == smallerValue:
            return largest, chunks

        quotient, remainder = divmod(biggerValue, smallerValue)

        if remainder == 0:
            count = quotient - 1
            if count:
                chunks.append((largest, bigger, count))
            baseLargest = largest if count % 2 == 0 else bigger
            return baseLargest, chunks

        chunks.append((largest, bigger, quotient))

        if quotient % 2:
            values[largest] = remainder
            values[bigger] = smallerValue + remainder
        else:
            values[largest] = smallerValue + remainder
            values[bigger] = remainder
        values[smaller] = smallerValue


def turnsUntilKnown(numbers):
    baseLargest, chunks = reductionChunks(numbers)
    turn = baseLargest + 1

    for firstPlayer, secondPlayer, count in reversed(chunks):
        if count % 2:
            turn = applyAlternatingTurns(turn, firstPlayer, secondPlayer, count)
        else:
            turn = applyAlternatingTurns(turn, secondPlayer, firstPlayer, count)

    return turn


@lru_cache(maxsize=None)
def slowTurnsUntilKnown(numbers):
    values = list(numbers)
    turn = 1

    while True:
        player = (turn - 1) % 3
        observed = [values[index] for index in range(3) if index != player]

        if observed[0] == observed[1]:
            return turn

        if values[player] == observed[0] + observed[1]:
            alternate = values[:]
            alternate[player] = abs(observed[0] - observed[1])
            if slowTurnsUntilKnown(tuple(alternate)) < turn:
                return turn

        turn += 1


def solve():
    total = 0
    for a in range(1, TARGET_A_LIMIT + 1):
        for b in range(1, TARGET_B_LIMIT + 1):
            first = a**b
            second = b**a
            total += turnsUntilKnown((first, second, first + second))
    return total


def runTests():
    assert turnsUntilKnown((2, 1, 1)) == 1
    assert turnsUntilKnown((2, 7, 5)) == 5

    for a in range(1, 20):
        for b in range(1, 20):
            triples = (
                (a, b, a + b),
                (a, a + b, b),
                (a + b, a, b),
            )
            for triple in triples:
                assert turnsUntilKnown(triple) == slowTurnsUntilKnown(triple)

    assert solve() == 70_228_218


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
