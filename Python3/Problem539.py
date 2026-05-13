from functools import cache
import time


MODULUS = 987_654_321


@cache
def survivor(n):
    if n == 1:
        return 1

    half = n // 2
    return 2 * (half + 1 - survivor(half))


@cache
def survivorSum(limit):
    if limit == 0:
        return 0
    if limit == 1:
        return 1

    half = limit // 2
    if limit % 2 == 1:
        return 1 + 2 * (half * (half + 3) - 2 * survivorSum(half))
    return 2 * half * half + 4 * half - 1 - 4 * survivorSum(half) + 2 * survivor(half)


def runTests():
    assert survivor(1) == 1
    assert survivor(9) == 6
    assert survivor(1_000) == 510
    assert survivorSum(1_000) == 268_271


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = survivorSum(10 ** 18) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
