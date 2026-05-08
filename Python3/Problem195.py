import math
import time


def multipleCount(radius_limit, radius_factor):
    return math.isqrt((4 * radius_limit * radius_limit) // (3 * radius_factor * radius_factor))


def alternateMultipleCount(radius_limit, radius_factor):
    return math.isqrt((12 * radius_limit * radius_limit) // (radius_factor * radius_factor))


def triangleCount(radius_limit):
    total = 0
    first_factor_limit = math.isqrt((4 * radius_limit * radius_limit) // 3)

    for n in range(1, first_factor_limit + 1):
        max_m = first_factor_limit // n
        if max_m <= n:
            break

        for m in range(n + 1, max_m + 1):
            if math.gcd(m, n) != 1 or (m - n) % 3 == 0:
                continue

            radius_factor = m * n
            total += multipleCount(radius_limit, radius_factor)

    second_factor_limit = math.isqrt(12 * radius_limit * radius_limit)

    for n in range(1, second_factor_limit + 1):
        if 3 * n + 1 > second_factor_limit:
            break

        m = n + 1
        while True:
            radius_factor = (m - n) * (m + 2 * n)
            if radius_factor > second_factor_limit:
                break

            if math.gcd(m, n) == 1 and (m - n) % 3 != 0:
                total += alternateMultipleCount(radius_limit, radius_factor)

            m += 1

    return total


def runTests():
    assert triangleCount(100) == 1234
    assert triangleCount(1000) == 22767
    assert triangleCount(10000) == 359912


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangleCount(1053779)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
