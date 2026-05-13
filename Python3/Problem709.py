import time


MODULUS = 1_020_202_009


def bagPackingCount(bags):
    previous = [1]

    for row in range(1, bags + 1):
        current = [0] * (row + 1)
        running = 0

        for column in range(1, row + 1):
            running += previous[row - column]
            if running >= MODULUS:
                running -= MODULUS
            current[column] = running

        previous = current

    return previous[-1]


def runTests():
    assert bagPackingCount(4) == 5
    assert bagPackingCount(8) == 1_385


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = bagPackingCount(24_680)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
