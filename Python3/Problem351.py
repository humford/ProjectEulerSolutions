import time
from array import array


LIMIT = 100_000_000
PRECOMPUTE_LIMIT = 1_000_000


def totientPrefix(limit):
    phi = array("Q", range(limit + 1))

    for number in range(2, limit + 1):
        if phi[number] == number:
            for multiple in range(number, limit + 1, number):
                phi[multiple] -= phi[multiple] // number

    prefix = array("Q", [0]) * (limit + 1)
    running = 0

    for number in range(1, limit + 1):
        running += phi[number]
        prefix[number] = running

    return prefix


def hiddenPoints(limit=LIMIT):
    prefix = totientPrefix(min(PRECOMPUTE_LIMIT, limit))
    cache = {}

    def summatoryTotient(number):
        if number < len(prefix):
            return prefix[number]

        if number in cache:
            return cache[number]

        total = number * (number + 1) // 2
        divisor = 2

        while divisor <= number:
            quotient = number // divisor
            nextDivisor = number // quotient
            total -= (nextDivisor - divisor + 1) * summatoryTotient(quotient)
            divisor = nextDivisor + 1

        cache[number] = total
        return total

    return 6 * (limit * (limit + 1) // 2 - summatoryTotient(limit))


def runTests():
    assert hiddenPoints(5) == 30
    assert hiddenPoints(10) == 138
    assert hiddenPoints(1000) == 1177848


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hiddenPoints()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
