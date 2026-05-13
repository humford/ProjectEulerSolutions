import math
import time


ROWS = 100
COLUMNS = 500


def mazeLog10(rows, columns):
    if rows == 1 and columns == 1:
        return 0.0

    total = 0.0

    for row in range(rows):
        for column in range(columns):
            if row == 0 and column == 0:
                continue

            eigenvalue = (
                4.0
                - 2.0 * math.cos(math.pi * row / rows)
                - 2.0 * math.cos(math.pi * column / columns)
            )
            total += math.log10(eigenvalue)

    return total - math.log10(rows * columns)


def mazeCountScientific(rows=ROWS, columns=COLUMNS):
    logarithm = mazeLog10(rows, columns)
    exponent = math.floor(logarithm)
    mantissa = 10 ** (logarithm - exponent)
    return "{:.4f}e{}".format(mantissa, exponent)


def runTests():
    assert mazeCountScientific(1, 1) == "1.0000e0"
    assert mazeCountScientific(2, 2) == "4.0000e0"
    assert mazeCountScientific(3, 4) == "2.4150e3"
    assert mazeCountScientific(9, 12) == "2.5720e46"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = mazeCountScientific()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
