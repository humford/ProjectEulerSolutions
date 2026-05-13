from math import gcd, isqrt, sqrt
import time


TARGET_R = 10**18


def bruteF(radius):
    best = 0
    limit = isqrt(2 * radius - 1)

    for m in range(2, limit + 1):
        for n in range(1, m):
            if (m - n) % 2 == 1 and gcd(m, n) == 1:
                if m * m + n * n < 2 * radius:
                    best = max(best, n * (m - n))

    return best


def continuousCanBeat(gap, radius, product):
    square = gap * gap
    return (
        2 * square * square
        - (4 * radius - 4 * product) * square
        + 4 * product * product
    ) < 0


def bestForGap(gap, radius):
    if gap <= 0 or gap % 2 == 0 or gap * gap >= 4 * radius:
        return 0

    v = isqrt(4 * radius - 1 - gap * gap)
    if v % 2 != gap % 2:
        v -= 1
    if v <= gap:
        return 0

    n = (v - gap) // 2
    while n > 0 and gcd(n, gap) != 1:
        n -= 1

    return n * gap


def F(radius):
    if radius < 10**6:
        return bruteF(radius)

    center = int(sqrt(2 - sqrt(2)) * sqrt(radius))
    best = 0
    bestGap = center | 1

    for gap in range(max(1, center - 20_000) | 1, center + 20_001, 2):
        product = bestForGap(gap, radius)
        if product > best:
            best = product
            bestGap = gap

    low = 1
    high = bestGap
    while low < high:
        middle = (low + high) // 2
        if continuousCanBeat(middle, radius, best):
            high = middle
        else:
            low = middle + 1
    left = low

    low = bestGap
    high = isqrt(4 * radius - 1)
    while low < high:
        middle = (low + high + 1) // 2
        if continuousCanBeat(middle, radius, best):
            low = middle
        else:
            high = middle - 1
    right = low

    for gap in range(left | 1, right + 1, 2):
        product = bestForGap(gap, radius)
        if product > best:
            best = product

    return best


def solve():
    return F(TARGET_R)


def runTests():
    assert F(100) == 36
    assert F(1_000) == bruteF(1_000)
    assert F(1_000_000) == bruteF(1_000_000)
    assert solve() == 414_213_562_371_805_310


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
