from collections import Counter
from pathlib import Path


HANDS_FILE = Path("Files/p054_poker.txt")
CARD_VALUES = {str(value): value for value in range(2, 10)}
CARD_VALUES.update({"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14})


def straightHighCard(values):
    unique = sorted(set(values), reverse=True)
    if unique == [14, 5, 4, 3, 2]:
        return 5
    if len(unique) == 5 and unique[0] - unique[-1] == 4:
        return unique[0]
    return None


def handRank(hand):
    values = sorted((CARD_VALUES[card[0]] for card in hand), reverse=True)
    suits = [card[1] for card in hand]
    counts = Counter(values)
    count_groups = sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True)
    straight_high = straightHighCard(values)
    is_flush = len(set(suits)) == 1

    if straight_high and is_flush:
        return 8, [straight_high]
    if count_groups[0][1] == 4:
        quad = count_groups[0][0]
        kicker = max(value for value in values if value != quad)
        return 7, [quad, kicker]
    if count_groups[0][1] == 3 and count_groups[1][1] == 2:
        return 6, [count_groups[0][0], count_groups[1][0]]
    if is_flush:
        return 5, values
    if straight_high:
        return 4, [straight_high]
    if count_groups[0][1] == 3:
        trip = count_groups[0][0]
        kickers = sorted((value for value in values if value != trip), reverse=True)
        return 3, [trip] + kickers
    if count_groups[0][1] == 2 and count_groups[1][1] == 2:
        pairs = sorted([count_groups[0][0], count_groups[1][0]], reverse=True)
        kicker = max(value for value in values if value not in pairs)
        return 2, pairs + [kicker]
    if count_groups[0][1] == 2:
        pair = count_groups[0][0]
        kickers = sorted((value for value in values if value != pair), reverse=True)
        return 1, [pair] + kickers
    return 0, values


def playerOneWins(line):
    cards = line.split()
    return handRank(cards[:5]) > handRank(cards[5:])


def countPlayerOneWins(path=HANDS_FILE):
    return sum(1 for line in path.read_text().splitlines() if line and playerOneWins(line))


def runTests():
    assert not playerOneWins("5H 5C 6S 7S KD 2C 3S 8S 8D TD")
    assert playerOneWins("5D 8C 9S JS AC 2C 5C 7D 8S QH")
    assert not playerOneWins("2D 9C AS AH AC 3D 6D 7D TD QD")
    assert playerOneWins("4D 6S 9H QH QC 3D 6D 7H QD QS")
    assert playerOneWins("2H 2D 4C 4D 4S 3C 3D 3S 9S 9D")


def solve():
    return countPlayerOneWins()


if __name__ == "__main__":
    runTests()
    print(solve())
