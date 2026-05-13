import time


LIMIT = 10**12


def strongRepunits(limit=LIMIT):
    values = {1}
    base = 2

    while 1 + base + base * base < limit:
        value = 1 + base + base * base

        while value < limit:
            values.add(value)
            value = value * base + 1

        base += 1

    return values


def strongRepunitSum(limit=LIMIT):
    return sum(strongRepunits(limit))


def runTests():
    assert sorted(strongRepunits(50)) == [1, 7, 13, 15, 21, 31, 40, 43]
    assert strongRepunitSum(1000) == 15864


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = strongRepunitSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
