import math
import time


LIMIT = 10**8


def rightTriangleCount(limit):
    total = 0
    m = 2

    while 2 * m * (m + 1) <= limit:
        for n in range(1, m):
            perimeter = 2 * m * (m + n)
            if perimeter > limit:
                break

            if (m - n) % 2 == 1 and math.gcd(m, n) == 1:
                total += limit // perimeter

        m += 1

    return total


def hundredTwentyDegreeTriangleCount(limit):
    total = 0
    m = 2

    while 2 * m * m + 3 * m + 1 <= limit:
        for n in range(1, m):
            perimeter = 2 * m * m + 3 * m * n + n * n
            if perimeter > limit:
                break

            if math.gcd(m, n) == 1 and (m - n) % 3 != 0:
                total += limit // perimeter

        m += 1

    return total


def sixtyDegreeTriangleCount(limit):
    total = limit // 3

    m = 3
    while 2 * m * m - m + 1 <= limit:
        for n in range(1, m // 2 + 1):
            perimeter = 2 * m * m + m * n - n * n
            if perimeter > limit:
                break

            if math.gcd(m, n) == 1 and (m + n) % 3 != 0:
                total += limit // perimeter

        m += 1

    m = 2
    while 3 * m * (m + 1) <= limit:
        for n in range(1, m):
            perimeter = 3 * m * (m + n)
            if perimeter > limit:
                break

            if math.gcd(m, n) == 1 and (m - n) % 3 != 0:
                total += limit // perimeter

        m += 1

    return total


def integralAngleTriangleCount(limit):
    return (
        rightTriangleCount(limit)
        + hundredTwentyDegreeTriangleCount(limit)
        + sixtyDegreeTriangleCount(limit)
    )


def bruteIntegralAngleTriangleCount(limit):
    total = 0

    for a in range(1, limit + 1):
        for b in range(a, limit + 1):
            for c in range(b, limit + 1):
                if a + b + c > limit:
                    break
                if a + b <= c:
                    continue

                sides = (a, b, c)
                for index, opposite in enumerate(sides):
                    adjacent = [sides[other] for other in range(3) if other != index]
                    x, y = adjacent

                    if (
                        opposite * opposite == x * x + y * y
                        or opposite * opposite == x * x + y * y - x * y
                        or opposite * opposite == x * x + y * y + x * y
                    ):
                        total += 1
                        break

    return total


def runTests():
    assert integralAngleTriangleCount(100) == bruteIntegralAngleTriangleCount(100)
    assert integralAngleTriangleCount(1000) == 1388


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = integralAngleTriangleCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
