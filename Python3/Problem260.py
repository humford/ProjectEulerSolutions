import time


LIMIT = 1000


def losingStoneSum(limit):
    full_mask = (1 << (limit + 1)) - 1
    at_least = [full_mask ^ ((1 << value) - 1) for value in range(limit + 1)]
    one_pile = [0] * (limit + 1)
    two_piles = [0] * (limit + 1)
    two_pile_columns = [0] * (limit + 1)
    three_piles = [0] * (limit + 1)
    total = 0

    for x in range(limit + 1):
        for y in range(x, limit + 1):
            if (one_pile[x] >> y) & 1:
                continue

            blocked = (
                one_pile[y]
                | one_pile[x]
                | two_piles[y - x]
                | (two_pile_columns[x] << y)
                | (two_pile_columns[y] << x)
                | (three_piles[y - x] << x)
            )
            available = (~blocked) & at_least[y]

            if not available:
                continue

            z = (available & -available).bit_length() - 1
            total += x + y + z

            one_pile[y] |= 1 << z
            one_pile[x] |= 1 << z
            one_pile[x] |= 1 << y

            first = y - x
            second = z
            two_piles[first] |= 1 << second
            two_pile_columns[second] |= 1 << first

            first = z - y
            second = x
            two_piles[first] |= 1 << second
            two_pile_columns[second] |= 1 << first

            first = z - x
            second = y
            two_piles[first] |= 1 << second
            two_pile_columns[second] |= 1 << first

            three_piles[y - x] |= 1 << (z - x)

    return total


def runTests():
    assert losingStoneSum(2) == 3
    assert losingStoneSum(100) == 173895


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = losingStoneSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
