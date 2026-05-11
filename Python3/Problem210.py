import math
import time

import numpy as np


def integerSquareRoot(values):
    roots = np.sqrt(values).astype(np.int64)
    roots += ((roots + 1) * (roots + 1) <= values)
    roots -= roots * roots > values
    return roots


def evenCircleContribution(half_center, chunk_size=5000000):
    max_square = 2 * half_center * half_center - 1
    x_max = math.isqrt(max_square)
    y_sum = 0

    for x_start in range(0, x_max + 1, chunk_size):
        x_stop = min(x_start + chunk_size, x_max + 1)
        x_values = np.arange(x_start, x_stop, dtype=np.int64)
        y_values = integerSquareRoot(np.int64(max_square) - x_values * x_values)
        y_sum += int(y_values.sum(dtype=np.int64))

    return 4 * y_sum - 2 * (half_center - 1)


def oddCircleContribution(center, chunk_size=5000000):
    max_square = 2 * center * center - 1
    x_max = math.isqrt(max_square)
    y_sum = 0

    for x_start in range(1, x_max + 1, 2 * chunk_size):
        x_stop = min(x_start + 2 * chunk_size, x_max + 1)
        x_values = np.arange(x_start, x_stop, 2, dtype=np.int64)
        y_values = integerSquareRoot(np.int64(max_square) - x_values * x_values)
        y_sum += int(((y_values + 1) // 2).sum(dtype=np.int64))

    return 4 * y_sum - (center - 1)


def circleContribution(radius):
    if radius % 4 != 0:
        raise ValueError("radius must be divisible by 4")

    center = radius // 4
    if center % 2 == 0:
        return evenCircleContribution(center // 2)

    return oddCircleContribution(center)


def obtuseTrianglePointCount(radius):
    return 3 * radius * radius // 2 + circleContribution(radius)


def bruteObtuseTrianglePointCount(radius):
    c = radius / 4
    total = 0

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if abs(x) + abs(y) > radius or x == y:
                continue

            obtuse_at_o = x + y < 0
            obtuse_at_c = x + y > 2 * c
            obtuse_at_b = x * x + y * y - c * (x + y) < 0

            if obtuse_at_o or obtuse_at_c or obtuse_at_b:
                total += 1

    return total


def runTests():
    assert bruteObtuseTrianglePointCount(4) == 24
    assert obtuseTrianglePointCount(4) == 24
    assert obtuseTrianglePointCount(8) == 100


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = obtuseTrianglePointCount(1000000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
