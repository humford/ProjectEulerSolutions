import time

import numpy as np


LIMIT = 100000


def angularBisectorTriangleCount(limit):
    total = 0

    for bc in range(1, limit // 3 + 1):
        ac = np.arange(bc, (limit - bc) // 2 + 1, dtype=np.int64)
        common = np.gcd(ac, bc)
        step = (bc + ac) // common
        maximum_ab = np.minimum(bc + ac - 1, limit - bc - ac)
        counts = maximum_ab // step - (ac - 1) // step
        total += int(counts.sum())

    return total


def bruteTriangleCount(limit):
    total = 0

    for bc in range(1, limit // 3 + 1):
        for ac in range(bc, (limit - bc) // 2 + 1):
            for ab in range(ac, min(bc + ac, limit - bc - ac + 1)):
                if ab * bc % (ac + bc) == 0:
                    total += 1

    return total


def runTests():
    assert angularBisectorTriangleCount(150) == bruteTriangleCount(150)
    assert angularBisectorTriangleCount(1000) == 61339


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = angularBisectorTriangleCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
