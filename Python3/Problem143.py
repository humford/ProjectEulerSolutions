import collections
import math
import time


def compatiblePairs(limit):
    adjacency = collections.defaultdict(set)
    max_m = math.isqrt(limit) + 1

    for m in range(2, max_m + 1):
        for n in range(1, m):
            first = m * m - n * n
            second = 2 * m * n + n * n
            if first <= 0:
                continue

            a, b = sorted((first, second))
            if a + b > limit:
                continue

            multiplier = 1
            while multiplier * (a + b) <= limit:
                pair_a = multiplier * a
                pair_b = multiplier * b
                adjacency[pair_a].add(pair_b)
                adjacency[pair_b].add(pair_a)
                multiplier += 1

    return adjacency


def torricelliSum(limit):
    adjacency = compatiblePairs(limit)
    sums = set()

    for p, p_neighbors in adjacency.items():
        for q in p_neighbors:
            if q <= p:
                continue
            if p + q >= limit:
                continue

            for r in p_neighbors & adjacency[q]:
                if r <= q:
                    continue
                total = p + q + r
                if total <= limit:
                    sums.add(total)

    return sum(sums)


def runTests():
    adjacency = compatiblePairs(20)
    assert 5 in adjacency[3]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = torricelliSum(120000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
