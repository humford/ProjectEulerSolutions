import math
import time


def g(n):
    count = 0
    maxY = math.isqrt(n // 41) + 2

    for y in range(-maxY, maxY + 1):
        discriminant = 4 * n - 163 * y * y
        if discriminant < 0:
            continue

        root = math.isqrt(discriminant)
        if root * root != discriminant:
            continue

        if (-y + root) % 2 == 0:
            count += 1
        if root != 0 and (-y - root) % 2 == 0:
            count += 1

    return count


def T(N):
    if N <= 0:
        return 0

    A = 4 * N
    B = 163
    maxY = math.isqrt(A // B)

    root0 = math.isqrt(A)
    total = root0 + 1 - (root0 & 1)

    bySquared = 0
    delta = B
    twoB = 2 * B

    for y in range(1, maxY + 1):
        bySquared += delta
        delta += twoB
        root = math.isqrt(A - bySquared)

        if y % 2:
            count = root + (root & 1)
        else:
            count = root + 1 - (root & 1)
        total += 2 * count

    return total - 1


def runTests():
    assert g(53) == 4
    assert T(10 ** 3) == 474
    assert T(10 ** 6) == 492_128


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = T(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
