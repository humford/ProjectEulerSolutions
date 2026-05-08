import functools
import time


@functools.lru_cache(maxsize=None)
def representationCount(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n % 2 == 1:
        return representationCount(n // 2)
    return representationCount(n // 2) + representationCount(n // 2 - 1)


def runTests():
    assert representationCount(10) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = representationCount(10 ** 25)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
