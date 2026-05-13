import math
import time


LIMIT = 100000000


def angularBisectorTriangleCount(limit):
    total = limit // 3
    gcd = math.gcd
    isqrt = math.isqrt

    x_limit = int(
        math.sqrt(limit * 2 / (3 + math.sqrt(2) + 2 / math.sqrt(2)))
    ) + 10
    for x in range(3, x_limit + 1):
        for y in range(x + 1, isqrt(2 * x * x) + 1):
            if gcd(x, y) != 1:
                continue

            if y & 1:
                scale = y
                a = scale * x
                b = scale * (x + y)
                c = x * (2 * x + y)
            else:
                scale = y // 2
                a = scale * x
                b = scale * (x + y)
                c = x * (2 * x + y) // 2

            perimeter = a + b + c
            if perimeter <= limit:
                total += limit // perimeter

    x_limit = int(
        math.sqrt(
            limit
            * 3
            / (1 + (1 + math.sqrt(3)) / 2 + (3 + math.sqrt(3)) / (2 * math.sqrt(3)))
        )
    ) + 10
    for x in range(2, x_limit + 1):
        x_odd = x & 1

        for y in range(x + 1, isqrt(3 * x * x) + 1):
            if gcd(x, y) != 1:
                continue

            if x_odd == 0:
                c_denominator = y // 3 if y % 3 == 0 else y
            elif y & 1:
                c_denominator = y // 3 if y % 3 == 0 else y
            else:
                c_denominator = 2 * y // 3 if y % 3 == 0 else 2 * y

            if (x + y) & 1:
                scale = c_denominator if c_denominator % 2 == 0 else 2 * c_denominator
            else:
                scale = c_denominator

            a = scale * x
            b = scale * (x + y) // 2
            c = scale * x * (3 * x + y) // (2 * y)
            perimeter = a + b + c

            if perimeter <= limit:
                total += limit // perimeter

    return total


def bruteAngularBisectorTriangleCount(limit):
    result = 0

    for a in range(1, limit // 3 + 1):
        for b in range(a, (limit - a) // 2 + 1):
            for c in range(b, min(a + b, limit - a - b + 1)):
                if ((a + b) * (a + c)) % (b * c) == 0:
                    result += 1

    return result


def runTests():
    assert angularBisectorTriangleCount(100) == bruteAngularBisectorTriangleCount(100)
    assert angularBisectorTriangleCount(200) == bruteAngularBisectorTriangleCount(200)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = angularBisectorTriangleCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
