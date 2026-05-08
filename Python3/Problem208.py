import functools
import time


def robotWalks(arcs):
    max_per_arc = arcs // 5

    @functools.cache
    def search(arcs_left, current_arc, counts):
        if arcs_left == 0:
            if current_arc != 0:
                return 0
            if counts[0] != counts[1] or counts[2] != counts[3] or counts[0] != counts[2]:
                return 0
            return 1

        total = 0
        for next_arc in ((current_arc + 1) % 5, (current_arc + 4) % 5):
            if counts[next_arc] < max_per_arc:
                next_counts = list(counts)
                next_counts[next_arc] += 1
                total += search(arcs_left - 1, next_arc, tuple(next_counts))

        return total

    return search(arcs, 0, (0, 0, 0, 0, 0))


def runTests():
    assert robotWalks(25) == 70932


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = robotWalks(70)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
