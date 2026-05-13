import itertools
import time


def possibleCoinRolls():
    return list(itertools.product((1, 2), repeat=2))


def possibleDiceRolls():
    return list(itertools.product(range(1, 7), repeat=2))


def rollChoiceMasks(cardCount, randomizer):
    rolls = possibleCoinRolls() if randomizer == "coins" else possibleDiceRolls()
    choices = []
    for x, y in rolls:
        options = {x, y, x + y}
        choices.append([1 << (option - 1) for option in options if option <= cardCount])
    return choices


def expectedTurnValue(cardCount, randomizer, tolerance=1e-12):
    goal = (1 << cardCount) - 1
    choicesByRoll = rollChoiceMasks(cardCount, randomizer)
    values = [0.0] * (goal + 1)

    while True:
        maxChange = 0.0
        for mask in range(goal):
            oldValue = values[mask]
            total = 0.0
            for choices in choicesByRoll:
                total += min(values[mask ^ choice] for choice in choices)
            values[mask] = 1.0 + total / len(choicesByRoll)
            maxChange = max(maxChange, abs(values[mask] - oldValue))

        if maxChange < tolerance:
            return values[0]


def expectedTurns(cardCount, randomizer):
    return f"{expectedTurnValue(cardCount, randomizer):.6f}"


def runTests():
    assert possibleCoinRolls() == list(itertools.product((1, 2), repeat=2))
    assert expectedTurns(4, "coins") == "5.673651"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedTurns(12, "dice")
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
