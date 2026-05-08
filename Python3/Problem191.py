import time


def prizeStringCount(days):
    counts = {(0, 0): 1}

    for _ in range(days):
        next_counts = {}
        for (late_count, trailing_absences), count in counts.items():
            next_counts[(late_count, 0)] = next_counts.get((late_count, 0), 0) + count

            if late_count == 0:
                next_counts[(1, 0)] = next_counts.get((1, 0), 0) + count

            if trailing_absences < 2:
                key = (late_count, trailing_absences + 1)
                next_counts[key] = next_counts.get(key, 0) + count

        counts = next_counts

    return sum(counts.values())


def runTests():
    assert prizeStringCount(4) == 43


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = prizeStringCount(30)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
