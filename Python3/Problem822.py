import heapq
import math
import time


MOD = 1_234_567_891


def S(n, rounds, modulus=MOD):
    heap = []
    maxLog = math.log(n)

    for value in range(2, n + 1):
        heap.append((math.log(value), value, value % modulus))
    heapq.heapify(heap)

    remaining = rounds
    while remaining and heap[0][0] * 2 < maxLog:
        logValue, order, residue = heapq.heappop(heap)
        logValue *= 2
        residue = residue * residue % modulus
        if logValue > maxLog:
            maxLog = logValue
        heapq.heappush(heap, (logValue, order, residue))
        remaining -= 1

    ordered = sorted(heap)
    quotient, remainder = divmod(remaining, n - 1)
    exponent = pow(2, quotient, modulus - 1)
    extraExponent = (2 * exponent) % (modulus - 1)

    total = 0
    for index, (_, __, residue) in enumerate(ordered):
        if index < remainder:
            total += pow(residue, extraExponent, modulus)
        else:
            total += pow(residue, exponent, modulus)

    return total % modulus


def runTests():
    assert S(5, 3) == 34
    assert S(10, 100) == 845_339_386


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10 ** 4, 10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
