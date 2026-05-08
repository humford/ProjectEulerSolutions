import math
import time

import numpy as np


def bruteSum(limit):
    total = 0

    for number in range(1, limit):
        sigma2 = sum(
            divisor * divisor
            for divisor in range(1, number + 1)
            if number % divisor == 0
        )
        root = math.isqrt(sigma2)
        if root * root == sigma2:
            total += number

    return total


def squareDivisorSum(limit, chunk_size=2000000):
    sigma2 = np.zeros(limit, dtype=np.uint64)

    for divisor in range(1, math.isqrt(limit - 1) + 1):
        square = divisor * divisor
        sigma2[square] += square

        max_counterpart = (limit - 1) // divisor
        start = divisor + 1
        while start <= max_counterpart:
            stop = min(max_counterpart + 1, start + chunk_size)
            counterparts = np.arange(start, stop, dtype=np.uint64)
            sigma2[divisor * start : divisor * stop : divisor] += (
                square + counterparts * counterparts
            )
            start = stop

    roots = np.sqrt(sigma2).astype(np.uint64)
    is_square = (roots * roots == sigma2) | ((roots + 1) * (roots + 1) == sigma2)
    return int(np.nonzero(is_square)[0].sum())


def runTests():
    assert squareDivisorSum(100, 20) == bruteSum(100)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squareDivisorSum(64000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
