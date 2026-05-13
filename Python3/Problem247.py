import heapq
import itertools
import math
import time


TARGET_LEFT = 3
TARGET_BELOW = 3


def sideLength(x, y):
    return 0.5 * (math.sqrt((x - y) * (x - y) + 4.0) - x - y)


def largestSquareIndex(target_left, target_below):
    counter = itertools.count()
    first_side = sideLength(1.0, 0.0)
    todo = [(-first_side, next(counter), 1.0, 0.0, 0, 0)]
    candidates = 1
    index = 0
    result = 0

    while candidates > 0:
        negative_side, _, x, y, left, below = heapq.heappop(todo)
        side = -negative_side
        index += 1

        if left == target_left and below == target_below:
            result = index

        top = (x, y + side, left, below + 1)
        right = (x + side, y, left + 1, below)

        for next_x, next_y, next_left, next_below in (top, right):
            next_side = sideLength(next_x, next_y)
            heapq.heappush(
                todo,
                (
                    -next_side,
                    next(counter),
                    next_x,
                    next_y,
                    next_left,
                    next_below,
                ),
            )

            if next_left <= target_left and next_below <= target_below:
                candidates += 1

        if left <= target_left and below <= target_below:
            candidates -= 1

    return result


def runTests():
    assert largestSquareIndex(0, 0) == 1
    assert largestSquareIndex(1, 1) == 50


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestSquareIndex(TARGET_LEFT, TARGET_BELOW)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
