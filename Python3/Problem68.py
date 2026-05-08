import itertools
import time


def ringString(outer, inner):
    start = min(range(5), key=lambda index: outer[index])
    parts = []

    for offset in range(5):
        index = (start + offset) % 5
        parts.extend([outer[index], inner[index], inner[(index + 1) % 5]])

    return "".join(str(part) for part in parts)


def maximumMagicFiveGonString():
    digits = set(range(1, 11))
    best = ""

    for inner in itertools.permutations(range(1, 10), 5):
        line_total_times_five = 55 + sum(inner)
        if line_total_times_five % 5 != 0:
            continue

        line_total = line_total_times_five // 5
        outer = [
            line_total - inner[index] - inner[(index + 1) % 5]
            for index in range(5)
        ]

        if set(outer) == digits - set(inner):
            candidate = ringString(outer, inner)
            if len(candidate) == 16 and candidate > best:
                best = candidate

    return best


def runTests():
    assert ringString([6, 10, 9, 8, 7], [5, 3, 1, 4, 2]) == "6531031914842725"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumMagicFiveGonString()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
