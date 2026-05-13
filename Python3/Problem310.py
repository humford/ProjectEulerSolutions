import math
import time
from collections import Counter


LIMIT = 100000


def grundyValues(limit):
    squares = [number * number for number in range(1, math.isqrt(limit) + 1)]
    values = [0] * (limit + 1)
    seen = [0] * 512

    for heap_size in range(1, limit + 1):
        stamp = heap_size

        for square in squares:
            if square > heap_size:
                break
            seen[values[heap_size - square]] = stamp

        mex = 0
        while seen[mex] == stamp:
            mex += 1

        values[heap_size] = mex

    return values


def losingPositionCount(limit):
    counts = Counter(grundyValues(limit))
    grundy_numbers = sorted(counts)
    total = 0

    for i, first in enumerate(grundy_numbers):
        for second in grundy_numbers[i:]:
            third = first ^ second

            if third < second or third not in counts:
                continue

            if first == second == third:
                count = counts[first]
                total += count * (count + 1) * (count + 2) // 6
            elif first == second:
                total += counts[third] * counts[first] * (counts[first] + 1) // 2
            elif second == third:
                total += counts[first] * counts[second] * (counts[second] + 1) // 2
            else:
                total += counts[first] * counts[second] * counts[third]

    return total


def runTests():
    assert losingPositionCount(29) == 1160


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = losingPositionCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
