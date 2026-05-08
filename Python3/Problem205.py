import time


def distribution(dice, sides):
    counts = {0: 1}

    for _ in range(dice):
        next_counts = {}
        for total, count in counts.items():
            for roll in range(1, sides + 1):
                next_counts[total + roll] = next_counts.get(total + roll, 0) + count
        counts = next_counts

    return counts


def winProbability():
    peter = distribution(9, 4)
    colin = distribution(6, 6)
    peter_total = 4 ** 9
    colin_total = 6 ** 6
    wins = 0

    for peter_sum, peter_count in peter.items():
        wins += peter_count * sum(
            colin_count
            for colin_sum, colin_count in colin.items()
            if colin_sum < peter_sum
        )

    return wins / (peter_total * colin_total)


def runTests():
    assert sum(distribution(2, 6).values()) == 36


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f"{winProbability():.7f}"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
