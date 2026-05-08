import time


def solutionCounts(limit):
    counts = [0] * limit

    for first_factor in range(1, limit):
        max_second = (limit - 1) // first_factor
        for second_factor in range(1, max_second + 1):
            if (first_factor + second_factor) % 4 != 0:
                continue
            if 3 * second_factor <= first_factor:
                continue
            counts[first_factor * second_factor] += 1

    return counts


def countWithSolutions(limit, target):
    return solutionCounts(limit).count(target)


def runTests():
    assert solutionCounts(2000)[1155] == 10


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = countWithSolutions(1000000, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
