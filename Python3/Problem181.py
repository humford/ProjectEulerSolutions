import time


def groupingCount(black_total, white_total):
    ways = [[0] * (white_total + 1) for _ in range(black_total + 1)]
    ways[0][0] = 1

    for group_black in range(black_total + 1):
        for group_white in range(white_total + 1):
            if group_black == 0 and group_white == 0:
                continue

            for black in range(group_black, black_total + 1):
                row = ways[black]
                previous_row = ways[black - group_black]
                for white in range(group_white, white_total + 1):
                    row[white] += previous_row[white - group_white]

    return ways[black_total][white_total]


def runTests():
    assert groupingCount(3, 1) == 7


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = groupingCount(60, 40)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
