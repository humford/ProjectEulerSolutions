import collections
import time


def rowsBySum():
    rows = collections.defaultdict(list)

    for value in range(10000):
        row = (
            value // 1000,
            (value // 100) % 10,
            (value // 10) % 10,
            value % 10,
        )
        rows[sum(row)].append(row)

    return rows


def crissCrossCount():
    total = 0

    for target_sum, rows in rowsBySum().items():
        bottom_pairs = collections.Counter()

        for third in rows:
            for fourth in rows:
                bottom_pairs[
                    (
                        third[0] + fourth[0],
                        third[1] + fourth[1],
                        third[2] + fourth[2],
                        third[3] + fourth[3],
                        third[2] + fourth[3],
                        third[1] + fourth[0],
                    )
                ] += 1

        for first in rows:
            for second in rows:
                total += bottom_pairs[
                    (
                        target_sum - first[0] - second[0],
                        target_sum - first[1] - second[1],
                        target_sum - first[2] - second[2],
                        target_sum - first[3] - second[3],
                        target_sum - first[0] - second[1],
                        target_sum - first[3] - second[2],
                    )
                ]

    return total


def runTests():
    assert len(rowsBySum()[0]) == 1
    assert len(rowsBySum()[36]) == 1


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = crissCrossCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
