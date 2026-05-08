import time


def minimumEncodingCost(symbols):
    leaves = 1
    total_cost = 0
    counts = {0: 1}
    current_cost = 0

    while leaves < symbols:
        while counts.get(current_cost, 0) == 0:
            current_cost += 1

        split_count = min(counts[current_cost], symbols - leaves)
        counts[current_cost] -= split_count
        counts[current_cost + 1] = counts.get(current_cost + 1, 0) + split_count
        counts[current_cost + 4] = counts.get(current_cost + 4, 0) + split_count
        total_cost += split_count * (current_cost + 5)
        leaves += split_count

    return total_cost


def runTests():
    assert minimumEncodingCost(6) == 35


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimumEncodingCost(10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
