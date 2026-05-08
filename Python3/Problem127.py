import math
import time


def radicals(limit):
    values = [1] * limit

    for n in range(2, limit):
        if values[n] == 1:
            for multiple in range(n, limit, n):
                values[multiple] *= n

    return values


def abcHitSum(limit):
    radical = radicals(limit)
    candidates = sorted(range(1, limit), key=lambda n: radical[n])
    total = 0

    for c in range(3, limit):
        radical_c = radical[c]

        for a in candidates:
            radical_a = radical[a]
            if radical_a * radical_c >= c:
                break
            if 2 * a >= c:
                continue
            if math.gcd(a, c) != 1:
                continue

            b = c - a
            if radical_a * radical[b] * radical_c < c:
                total += c

    return total


def runTests():
    assert abcHitSum(1000) == 12523


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = abcHitSum(120000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
