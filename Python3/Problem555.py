import functools
import time


@functools.lru_cache(None)
def mccarthy91(n):
    if n > 100:
        return n - 10
    return mccarthy91(mccarthy91(n + 11))


def generalizedMccarthy(m, k, s):
    @functools.lru_cache(None)
    def evaluate(n):
        if n > m:
            return n - s
        return evaluate(evaluate(n + k))

    return evaluate


def bruteFixedPointSum(m, k, s):
    evaluate = generalizedMccarthy(m, k, s)
    return sum(n for n in range(m + 1) if evaluate(n) == n)


def fixedPointSum(m, k, s):
    step = k - s
    if s % step != 0:
        return 0

    first = max(m - s + 1, 0)
    last = m - s + step
    if first > last:
        return 0

    count = last - first + 1
    return count * (first + last) // 2


def generalizedFixedPointSum(p, m):
    total = 0
    for step in range(1, p // 2 + 1):
        quotientLimit = p // step - 1
        total += (
            step
            * quotientLimit
            * (2 * m + 1 - step * quotientLimit)
            // 2
        )
    return total


def runTests():
    assert [n for n in range(200) if mccarthy91(n) == n] == [91]
    assert fixedPointSum(100, 11, 10) == 91
    for m in range(1, 12):
        for k in range(2, 12):
            for s in range(1, k):
                assert fixedPointSum(m, k, s) == bruteFixedPointSum(m, k, s)

    assert generalizedFixedPointSum(10, 10) == 225
    assert generalizedFixedPointSum(1_000, 1_000) == 208_724_467


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = generalizedFixedPointSum(10 ** 6, 10 ** 6)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
