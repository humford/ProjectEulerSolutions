import math
import time
from array import array


LIMIT = 10_000_000
MODULUS = 1_000_000_007


def factorialTables(limit):
    factorial = array("I", [1]) * (limit + 1)

    for number in range(1, limit + 1):
        factorial[number] = (factorial[number - 1] * number) % MODULUS

    inverse = array("I", [1]) * (limit + 1)
    inverse[limit] = pow(factorial[limit], MODULUS - 2, MODULUS)

    for number in range(limit, 0, -1):
        inverse[number - 1] = (inverse[number] * number) % MODULUS

    return factorial, inverse


def choose(n, k, factorial, inverse):
    if k < 0 or k > n:
        return 0

    return factorial[n] * inverse[k] % MODULUS * inverse[n - k] % MODULUS


def inadmissiblePoints(limit):
    root = math.isqrt(limit)
    squareSums = {number * number for number in range(1, math.isqrt(2 * limit) + 1)}
    points = []

    for xRoot in range(1, root + 1):
        x = xRoot * xRoot

        for yRoot in range(1, root + 1):
            y = yRoot * yRoot

            if x + y in squareSums:
                points.append((x, y))

    points.sort(key=lambda point: (point[0] + point[1], point[0]))
    return points


def admissiblePaths(limit=LIMIT):
    points = inadmissiblePoints(limit)
    points.append((limit, limit))
    factorial, inverse = factorialTables(2 * limit)
    ways = []

    for index, (x, y) in enumerate(points):
        count = choose(x + y, x, factorial, inverse)

        for previousIndex in range(index):
            previousX, previousY = points[previousIndex]

            if previousX <= x and previousY <= y:
                count -= ways[previousIndex] * choose(
                    x - previousX + y - previousY,
                    x - previousX,
                    factorial,
                    inverse,
                )
                count %= MODULUS

        ways.append(count)

    return ways[-1]


def runTests():
    assert admissiblePaths(5) == 252
    assert admissiblePaths(16) == 596994440
    assert admissiblePaths(1000) == 341920854


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = admissiblePaths()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
