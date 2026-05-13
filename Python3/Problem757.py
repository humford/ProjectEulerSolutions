import time
from heapq import heapify, heappop, heapreplace
from math import isqrt


def inversePronic(limit):
    return (isqrt(4 * limit + 1) - 1) // 2


def isStealthy(value):
    x = 1
    while True:
        pronic = x * (x + 1)
        if pronic * pronic > value:
            return False
        if value % pronic == 0:
            quotient = value // pronic
            y = inversePronic(quotient)
            if y * (y + 1) == quotient:
                return True
        x += 1


def bruteStealthyCount(limit):
    return sum(1 for value in range(1, limit + 1) if isStealthy(value))


def stealthyCount(limit):
    heap = []
    x = 1
    while True:
        base = x * (x + 1)
        if base * base > limit:
            break
        yMax = inversePronic(limit // base)
        heap.append((base * base, base, x, yMax))
        x += 1

    heapify(heap)
    count = 0
    previous = None
    while heap:
        value, base, y, yMax = heap[0]
        if value != previous:
            count += 1
            previous = value

        y += 1
        if y <= yMax:
            heapreplace(heap, (base * y * (y + 1), base, y, yMax))
        else:
            heappop(heap)

    return count


def runTests():
    assert isStealthy(36)
    assert bruteStealthyCount(200) == 12
    assert stealthyCount(200) == 12
    assert stealthyCount(10 ** 6) == 2_851


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = stealthyCount(10 ** 14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
