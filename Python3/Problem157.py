import math
import time


def divisorCount(n):
    count = 1
    factor = 2

    while factor * factor <= n:
        exponent = 0
        while n % factor == 0:
            exponent += 1
            n //= factor
        if exponent:
            count *= exponent + 1
        factor += 1 if factor == 2 else 2

    if n > 1:
        count *= 2

    return count


def powerTenDivisors(n):
    return sorted({2 ** twos * 5 ** fives for twos in range(n + 1) for fives in range(n + 1)})


def solutionCount(n):
    power = 10 ** n
    divisors = powerTenDivisors(n)
    count = 0

    for x in divisors:
        for y in divisors:
            if x > y:
                continue
            if math.gcd(x, y) == 1 and power % (x * y) == 0:
                count += divisorCount(power // (x * y) * (x + y))

    return count


def totalSolutionCount(limit):
    return sum(solutionCount(n) for n in range(1, limit + 1))


def runTests():
    assert solutionCount(1) == 20


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totalSolutionCount(9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
