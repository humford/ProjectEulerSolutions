import time
from functools import lru_cache


def fibonacciNumbersPast(limit):
    values = [0, 1, 2]
    while values[-1] <= limit:
        values.append(values[-1] + values[-2])
    return values


def fibonacciSubsetCount(limit):
    if limit < 0:
        return 0

    fibonacci = fibonacciNumbersPast(limit)
    maxIndex = len(fibonacci) - 2
    while len(fibonacci) <= maxIndex + 2:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    def prefixSum(index):
        if index <= 0:
            return 0
        return fibonacci[index + 2] - 2

    @lru_cache(maxsize=None)
    def count(index, capacity):
        if capacity < 0:
            return 0
        if index == 0:
            return 1
        if capacity >= prefixSum(index):
            return 1 << index
        if capacity < fibonacci[index]:
            return count(index - 1, capacity)
        return count(index - 1, capacity) + count(index - 1, capacity - fibonacci[index])

    return count(maxIndex, limit)


def runTests():
    assert fibonacciSubsetCount(100) == 415
    assert fibonacciSubsetCount(10_000) == 312_807


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciSubsetCount(10 ** 13)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
