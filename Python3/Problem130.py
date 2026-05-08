import math
import time


def isPrime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def repunitDivisibilityLength(n):
    remainder = 1 % n
    length = 1
    while remainder != 0:
        remainder = (remainder * 10 + 1) % n
        length += 1
    return length


def compositeRepunitValues(count):
    values = []
    n = 3

    while len(values) < count:
        if math.gcd(n, 10) == 1 and not isPrime(n):
            length = repunitDivisibilityLength(n)
            if (n - 1) % length == 0:
                values.append(n)
        n += 2

    return values


def runTests():
    assert compositeRepunitValues(5) == [91, 259, 451, 481, 703]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sum(compositeRepunitValues(25))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
