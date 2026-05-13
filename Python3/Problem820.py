import time


def nthDigitOfReciprocal(n, denominator):
    return 10 * pow(10, n - 1, denominator) // denominator


def S(n):
    total = 0
    for denominator in range(1, n + 1):
        total += nthDigitOfReciprocal(n, denominator)
    return total


def runTests():
    assert nthDigitOfReciprocal(7, 1) == 0
    assert nthDigitOfReciprocal(7, 2) == 0
    assert nthDigitOfReciprocal(7, 4) == 0
    assert nthDigitOfReciprocal(7, 5) == 0
    assert nthDigitOfReciprocal(7, 3) == 3
    assert nthDigitOfReciprocal(7, 6) == 6
    assert nthDigitOfReciprocal(7, 7) == 1
    assert S(7) == 10
    assert S(100) == 418


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
