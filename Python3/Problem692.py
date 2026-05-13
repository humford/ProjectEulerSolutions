import time
from bisect import bisect_right


TARGET = 23_416_728_348_467_685


def fibonacciUpTo(limit):
    values = [1, 2]
    while values[-1] <= limit:
        values.append(values[-1] + values[-2])
    return values


def minimalWinningMove(pebbles):
    fibonacci = fibonacciUpTo(pebbles)
    smallest = 0
    remaining = pebbles
    while remaining:
        index = bisect_right(fibonacci, remaining) - 1
        smallest = fibonacci[index]
        remaining -= smallest
    return smallest


def prefixBeforeFibonacci(fibonacci):
    prefix = [0] * len(fibonacci)
    if len(fibonacci) > 1:
        prefix[1] = 1
    for index in range(1, len(fibonacci) - 1):
        prefix[index + 1] = prefix[index] + fibonacci[index] + prefix[index - 1]
    return prefix


def minimalWinningMoveSum(limit):
    fibonacci = fibonacciUpTo(limit)
    prefix = prefixBeforeFibonacci(fibonacci)
    memo = {0: 0}

    def compute(value):
        if value in memo:
            return memo[value]
        index = bisect_right(fibonacci, value) - 1
        result = prefix[index] + fibonacci[index] + compute(value - fibonacci[index])
        memo[value] = result
        return result

    return compute(limit)


def runTests():
    assert minimalWinningMove(1) == 1
    assert minimalWinningMove(4) == 1
    assert minimalWinningMove(17) == 1
    assert minimalWinningMove(8) == 8
    assert minimalWinningMove(18) == 5
    assert minimalWinningMoveSum(13) == 43


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimalWinningMoveSum(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
