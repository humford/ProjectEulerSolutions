import collections
import math
import time


def isSquare(n):
    if n <= 0:
        return False
    root = math.isqrt(n)
    return root * root == n


def squareDifferenceValues(bound):
    values_by_x = collections.defaultdict(list)
    max_root = math.isqrt(2 * bound) + 1

    for high_root in range(2, max_root + 1):
        high_square = high_root * high_root
        for low_root in range(1, high_root):
            if (high_root + low_root) % 2 == 1:
                continue

            low_square = low_root * low_root
            x = (high_square + low_square) // 2
            value = (high_square - low_square) // 2
            if x <= bound:
                values_by_x[x].append(value)

    return values_by_x


def smallestSquareCollectionSum():
    bound = 1000

    while True:
        best = None
        values_by_x = squareDifferenceValues(bound)

        for x, values in values_by_x.items():
            values = sorted(values, reverse=True)
            for first_index, y in enumerate(values):
                for z in values[first_index + 1 :]:
                    if isSquare(y + z) and isSquare(y - z):
                        candidate = x + y + z
                        if best is None or candidate < best:
                            best = candidate

        if best is not None:
            return best
        bound *= 2


def runTests():
    assert isSquare(144)
    assert not isSquare(145)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smallestSquareCollectionSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
