import time


LIMIT = 10**6
PERIOD_START = 53
PERIOD = 34
PRECOMPUTE_LIMIT = 200


def grundyValues(limit):
    values = [0] * (limit + 1)

    for length in range(2, limit + 1):
        reachable = {
            values[left] ^ values[length - 2 - left] for left in range(length - 1)
        }
        mex = 0

        while mex in reachable:
            mex += 1

        values[length] = mex

    return values


def winningLengthCount(limit):
    grundy = grundyValues(PRECOMPUTE_LIMIT)

    if limit < PERIOD_START:
        return sum(1 for length in range(1, limit + 1) if grundy[length] != 0)

    total = sum(1 for length in range(1, PERIOD_START) if grundy[length] != 0)
    periodic_length = limit - PERIOD_START + 1
    period_wins = sum(
        1 for offset in range(PERIOD) if grundy[PERIOD_START + offset] != 0
    )

    total += (periodic_length // PERIOD) * period_wins
    total += sum(
        1
        for offset in range(periodic_length % PERIOD)
        if grundy[PERIOD_START + offset] != 0
    )

    return total


def runTests():
    assert winningLengthCount(5) == 3
    assert winningLengthCount(50) == 40


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningLengthCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
