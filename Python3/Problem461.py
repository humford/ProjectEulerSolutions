import bisect
import heapq
import math
import time


PI = math.pi


def functionValues(n):
    values = []
    k = 0
    while True:
        value = math.exp(k / n) - 1
        if value > PI:
            break
        values.append(value)
        k += 1
    return values


def _search_g(n):
    values = functionValues(n)

    pairs = []
    for a, va in enumerate(values):
        for b in range(a, len(values)):
            pairs.append((va + values[b], a * a + b * b))
    pairs.sort()
    sums = [pair[0] for pair in pairs]

    best_error = float("inf")
    best_g = None
    for pair_sum, pair_square_sum in pairs:
        target = PI - pair_sum
        index = bisect.bisect_left(sums, target)
        for candidate in (index - 1, index):
            if 0 <= candidate < len(pairs):
                other_sum, other_square_sum = pairs[candidate]
                error = abs(pair_sum + other_sum - PI)
                if error < best_error:
                    best_error = error
                    best_g = pair_square_sum + other_square_sum
    return best_g


def pairLimits(values):
    limits = []
    b = len(values) - 1
    for a, value in enumerate(values):
        if b < a:
            b = a
        while b >= a and value + values[b] > PI:
            b -= 1
        limits.append(b)
    return limits


def streamedPairSearch(n):
    values = functionValues(n)
    limits = pairLimits(values)
    lowHeap = []
    highHeap = []

    for a, maxB in enumerate(limits):
        if maxB >= a:
            heapq.heappush(lowHeap, (values[a] + values[a], a, a))
            heapq.heappush(highHeap, (-(values[a] + values[maxB]), a, maxB))

    low = heapq.heappop(lowHeap)
    high = heapq.heappop(highHeap)
    bestError = PI
    bestSquareSum = None

    while low[0] <= -high[0]:
        total = low[0] - high[0]
        error = abs(total - PI)
        if error < bestError:
            bestError = error
            bestSquareSum = low[1] * low[1] + low[2] * low[2] + high[1] * high[1] + high[2] * high[2]

        if total < PI:
            _, a, b = low
            nextB = b + 1
            if nextB <= limits[a]:
                heapq.heappush(lowHeap, (values[a] + values[nextB], a, nextB))
            low = heapq.heappop(lowHeap)
        else:
            _, a, b = high
            nextB = b - 1
            if nextB >= a:
                heapq.heappush(highHeap, (-(values[a] + values[nextB]), a, nextB))
            high = heapq.heappop(highHeap)

    return bestSquareSum


def almostPi(n):
    return streamedPairSearch(n)


def runTests():
    assert _search_g(200) == 64_658
    assert almostPi(200) == 64_658


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = almostPi(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
