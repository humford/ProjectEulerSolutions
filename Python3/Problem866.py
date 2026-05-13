from fractions import Fraction
import time


MOD = 987_654_319


def hexagonal(n):
    return n * (2 * n - 1)


def expectedProduct(n, modulus=MOD):
    expected = [0] * (n + 1)
    expected[0] = 1

    for size in range(1, n + 1):
        total = 0
        for leftSize in range(size):
            rightSize = size - 1 - leftSize
            total += expected[leftSize] * expected[rightSize]

        expected[size] = (
            hexagonal(size)
            * total
            * pow(size, -1, modulus)
        ) % modulus

    return expected[n]


def expectedProductExact(n):
    expected = [Fraction(0) for _ in range(n + 1)]
    expected[0] = Fraction(1)

    for size in range(1, n + 1):
        total = sum(
            expected[leftSize] * expected[size - 1 - leftSize]
            for leftSize in range(size)
        )
        expected[size] = Fraction(hexagonal(size), size) * total

    return expected[n]


def runTests():
    assert expectedProductExact(4) == 994
    assert expectedProduct(4) == 994


def solve():
    return expectedProduct(100)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
