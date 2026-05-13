import functools
import time


MODULUS = 10 ** 9


@functools.lru_cache(None)
def weirdFunction(n):
    if n == 1:
        return 1
    if n == 3:
        return 3
    if n % 2 == 0:
        return weirdFunction(n // 2)
    if n % 4 == 1:
        q = (n - 1) // 4
        return 2 * weirdFunction(2 * q + 1) - weirdFunction(q)
    q = (n - 3) // 4
    return 3 * weirdFunction(2 * q + 1) - 2 * weirdFunction(q)


def _oddFunction(k):
    return weirdFunction(2 * k + 1)


@functools.lru_cache(None)
def _oddPrefix(count):
    if count <= 0:
        return 0
    if count == 1:
        return 1
    if count % 2 == 0:
        half = count // 2
        return 5 * _oddPrefix(half) - 3 * prefixSum(half - 1) - 1

    half = count // 2
    return _oddPrefix(2 * half) + 2 * _oddFunction(half) - weirdFunction(half)


@functools.lru_cache(None)
def prefixSum(n):
    if n <= 0:
        return 0

    half = n // 2
    total = _oddPrefix(half) + prefixSum(half)
    if n % 2 == 1:
        total += _oddFunction(half)
    return total


def runTests():
    assert prefixSum(8) == 22
    assert prefixSum(100) == 3604


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = prefixSum(3 ** 37) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
