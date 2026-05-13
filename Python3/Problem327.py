import time


ROOMS = 30
MAX_CARDS = 40


def minimumCards(cards, rooms):
    needed = 1
    transport = cards - 2

    for _ in range(rooms):
        consumed = 0

        if needed >= cards:
            moves = (needed - cards) // transport

            if needed - moves * transport >= cards:
                moves += 1

            needed -= moves * transport
            consumed += moves * cards

        needed = needed + consumed + 1

    return needed


def roomDoomSum(rooms=ROOMS, maxCards=MAX_CARDS):
    return sum(minimumCards(cards, rooms) for cards in range(3, maxCards + 1))


def runTests():
    assert minimumCards(3, 3) == 6
    assert minimumCards(3, 6) == 123
    assert minimumCards(4, 6) == 23
    assert roomDoomSum(6, 4) == 146
    assert roomDoomSum(10, 10) == 10382


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roomDoomSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
