import collections
import time


def digitStringCount(length):
    counts = collections.Counter((digit, 0) for digit in range(1, 10))

    for position in range(1, length):
        next_counts = collections.Counter()
        for (last, previous), count in counts.items():
            for digit in range(10):
                if position < 2 or previous + last + digit <= 9:
                    next_counts[(digit, last)] += count
        counts = next_counts

    return sum(counts.values())


def runTests():
    assert digitStringCount(3) == 165


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = digitStringCount(20)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
