import math
import time


def tilingPythagoreanCount(limit):
    count = 0
    max_m = int((limit // 2) ** 0.5) + 1

    for m in range(2, max_m + 1):
        for n in range(1, m):
            if (m + n) % 2 == 0 or math.gcd(m, n) != 1:
                continue

            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            perimeter = a + b + c
            if perimeter >= limit:
                break

            if c % abs(a - b) == 0:
                count += (limit - 1) // perimeter

    return count


def runTests():
    assert tilingPythagoreanCount(100) == 9


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = tilingPythagoreanCount(100000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
