import heapq
import time


SEEDS = [
    (17, 7),
    (32, 14),
    (112, 50),
    (217, 97),
    (767, 343),
    (1487, 665),
]


def advanceSolution(x, y):
    return 161 * x + 360 * y, 72 * x + 161 * y


def nuggetFromX(x):
    return (x - 7) // 5


def modifiedGoldenNuggets(count):
    heap = [(nuggetFromX(x), x, y) for x, y in SEEDS]
    heapq.heapify(heap)
    nuggets = []
    seen = set()

    while len(nuggets) < count:
        nugget, x, y = heapq.heappop(heap)
        if nugget not in seen:
            seen.add(nugget)
            nuggets.append(nugget)

        next_x, next_y = advanceSolution(x, y)
        heapq.heappush(heap, (nuggetFromX(next_x), next_x, next_y))

    return nuggets


def runTests():
    assert modifiedGoldenNuggets(10) == [2, 5, 21, 42, 152, 296, 1050, 2037, 7205, 13970]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sum(modifiedGoldenNuggets(30))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
