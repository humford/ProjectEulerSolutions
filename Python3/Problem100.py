import time


def blueDiscsAbove(total_limit):
    blue = 1
    total = 1

    while total <= total_limit:
        blue, total = 3 * blue + 2 * total - 2, 4 * blue + 3 * total - 3

    return blue


def runTests():
    assert blueDiscsAbove(100) == 85


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = blueDiscsAbove(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
