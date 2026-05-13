import itertools
import time


MODULUS = 1_008_691_207


def hasOpenPath(pawns, size):
    if (0, 0) in pawns or (size - 1, size - 1) in pawns:
        return False

    reachable = set()
    for row in range(size):
        for column in range(size):
            if (row, column) in pawns:
                continue
            if (row, column) == (0, 0):
                reachable.add((row, column))
            elif (
                (row > 0 and (row - 1, column) in reachable) or
                (column > 0 and (row, column - 1) in reachable)
            ):
                reachable.add((row, column))

    return (size - 1, size - 1) in reachable


def openPositionCountBrute(size):
    count = 0
    for columns in itertools.permutations(range(size)):
        pawns = set(enumerate(columns))
        if hasOpenPath(pawns, size):
            count += 1
    return count


def coefficientForOpenPositionFormula(offset):
    if offset == 0:
        return 1
    if offset == 1:
        return -2
    return offset - 3


def openPositionCount(size, modulus=MODULUS):
    # If P(z)=sum n!z^n, the open positions are the coefficients of
    # P(z)((1-2z)/(1-z))^2 - (1-2z)/(1-z).
    factorial = 1
    total = 0
    for term in range(size + 1):
        if term:
            factorial = factorial * term % modulus
        offset = size - term
        total += factorial * coefficientForOpenPositionFormula(offset)
        total %= modulus

    return (total + (1 if size >= 1 else -1)) % modulus


def runTests():
    assert openPositionCountBrute(3) == 2
    assert openPositionCountBrute(5) == 70
    for size in range(1, 9):
        assert openPositionCount(size) == openPositionCountBrute(size)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = openPositionCount(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
