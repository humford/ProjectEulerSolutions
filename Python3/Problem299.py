import math
import time


LIMIT = 10**8


def incenterCaseCount(limit):
    total = 0
    n = 2

    while True:
        if 2 * n + 1 >= limit:
            break

        for m in range(1, n):
            if (m + n) % 2 == 0 or math.gcd(m, n) != 1:
                continue

            b = n * n - m * m
            d = 2 * n * m
            perimeter_part = b + d

            if perimeter_part >= limit:
                if m == 1:
                    return total
                continue

            count = (limit - 1) // perimeter_part
            total += count if b == d else 2 * count

        n += 1

    return total


def parallelCaseCount(limit):
    total = 0
    n = 1

    while 2 * (n * n + 2 * n + 2) < limit:
        m = 1

        while True:
            g = 2 * n * m
            a = n * n + 2 * m * m
            b = g + a

            if 2 * b >= limit:
                break

            if math.gcd(m, n) == 1:
                total += (limit - 1) // (2 * b)

            m += 1

        n += 2

    return total


def similarTriangleTripletCount(limit):
    return incenterCaseCount(limit) + parallelCaseCount(limit)


def runTests():
    assert similarTriangleTripletCount(100) == 92
    assert similarTriangleTripletCount(100000) == 320471


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = similarTriangleTripletCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
