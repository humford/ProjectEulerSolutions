import collections
import time


BOARD_SIZE = 40
GO = 0
JAIL = 10
G2J = 30
COMMUNITY_CHEST = {2, 17, 33}
CHANCE = {7, 22, 36}
RAILROADS = [5, 15, 25, 35]
UTILITIES = [12, 28]


def nextSquare(position, squares):
    for square in squares:
        if square > position:
            return square
    return squares[0]


def addWeighted(results, position, probability):
    for final_position, final_probability in resolveSquare(position):
        results[final_position] += probability * final_probability


def resolveSquare(position):
    if position == G2J:
        return [(JAIL, 1.0)]

    if position in COMMUNITY_CHEST:
        return [(GO, 1 / 16), (JAIL, 1 / 16), (position, 14 / 16)]

    if position in CHANCE:
        results = collections.defaultdict(float)
        direct_moves = [GO, JAIL, 11, 24, 39, 5]

        for square in direct_moves:
            addWeighted(results, square, 1 / 16)

        addWeighted(results, nextSquare(position, RAILROADS), 2 / 16)
        addWeighted(results, nextSquare(position, UTILITIES), 1 / 16)
        addWeighted(results, (position - 3) % BOARD_SIZE, 1 / 16)
        results[position] += 6 / 16
        return list(results.items())

    return [(position, 1.0)]


def diceOutcomes(sides):
    outcomes = []
    for first in range(1, sides + 1):
        for second in range(1, sides + 1):
            outcomes.append((first + second, first == second, 1 / (sides * sides)))
    return outcomes


def stationaryDistribution(sides, iterations=200):
    state_count = BOARD_SIZE * 3
    probabilities = [0.0] * state_count
    probabilities[GO] = 1.0
    outcomes = diceOutcomes(sides)

    for _ in range(iterations):
        next_probabilities = [0.0] * state_count

        for state, probability in enumerate(probabilities):
            if probability == 0.0:
                continue

            position = state % BOARD_SIZE
            doubles = state // BOARD_SIZE

            for roll, is_double, roll_probability in outcomes:
                if is_double and doubles == 2:
                    next_probabilities[JAIL] += probability * roll_probability
                    continue

                next_doubles = doubles + 1 if is_double else 0
                raw_position = (position + roll) % BOARD_SIZE
                for final_position, square_probability in resolveSquare(raw_position):
                    next_probabilities[next_doubles * BOARD_SIZE + final_position] += (
                        probability * roll_probability * square_probability
                    )

        probabilities = next_probabilities

    square_probabilities = [0.0] * BOARD_SIZE
    for state, probability in enumerate(probabilities):
        square_probabilities[state % BOARD_SIZE] += probability
    return square_probabilities


def modalString(sides):
    probabilities = stationaryDistribution(sides)
    top_squares = sorted(range(BOARD_SIZE), key=lambda square: probabilities[square], reverse=True)[:3]
    return "".join(str(square).zfill(2) for square in top_squares)


def runTests():
    assert nextSquare(7, RAILROADS) == 15
    assert nextSquare(36, RAILROADS) == 5
    assert modalString(6)[:2] == "10"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = modalString(4)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
