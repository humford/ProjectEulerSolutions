import math
import time


def pairCountForSum(total, maximum_side):
    lower = max(1, total - maximum_side)
    upper = total // 2
    return max(0, upper - lower + 1)


def integerShortestPathsAt(maximum_side):
    count = 0

    for side_sum in range(2, 2 * maximum_side + 1):
        root = math.isqrt(side_sum * side_sum + maximum_side * maximum_side)
        if root * root == side_sum * side_sum + maximum_side * maximum_side:
            count += pairCountForSum(side_sum, maximum_side)

    return count


def leastMExceeding(target):
    total = 0
    maximum_side = 0

    while total <= target:
        maximum_side += 1
        total += integerShortestPathsAt(maximum_side)

    return maximum_side


def runTests():
    assert leastMExceeding(2000) == 100


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastMExceeding(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
