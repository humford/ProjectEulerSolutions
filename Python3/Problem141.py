import math
import time


def isSquare(n):
    root = math.isqrt(n)
    return root * root == n


def progressiveSquareSum(limit):
    values = set()
    max_a = int(round(limit ** (1 / 3))) + 2

    for a in range(2, max_a + 1):
        a_cubed = a ** 3
        if a_cubed >= limit:
            break

        for b in range(1, a):
            if math.gcd(a, b) != 1:
                continue

            k = 1
            while True:
                value = k * k * a_cubed * b + k * b * b
                if value >= limit:
                    break
                if isSquare(value):
                    values.add(value)
                k += 1

    return sum(values)


def runTests():
    assert progressiveSquareSum(1000) == 9


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = progressiveSquareSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
