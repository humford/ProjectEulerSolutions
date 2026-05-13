import math
import time


LIMIT = 10**12
TERMS = 30


def cappedCombination(n, r, cap):
    if r < 0 or r > n:
        return 0

    r = min(r, n - r)
    value = 1

    for index in range(1, r + 1):
        value = value * (n - r + index) // index

        if value >= cap:
            return cap

    return value


def capacity(budget, lowerCost, higherCost, cap):
    total = 0
    lowerAnswers = int(budget / lowerCost)

    for lowerCount in range(lowerAnswers + 1):
        remaining = budget - lowerCount * lowerCost

        if remaining < 0:
            break

        higherCount = int(remaining / higherCost)
        total += cappedCombination(
            lowerCount + higherCount + 1,
            lowerCount + 1,
            cap - total,
        )

        if total >= cap:
            return cap

    return total


def optimalCost(size, lowerCost, higherCost):
    low = 0.0
    high = max(lowerCost, higherCost)

    while capacity(high, lowerCost, higherCost, size) < size:
        high *= 2

    for _ in range(100):
        middle = (low + high) / 2

        if capacity(middle, lowerCost, higherCost, size) >= size:
            high = middle
        else:
            low = middle

    best = high
    searchLimit = int((high + max(lowerCost, higherCost)) / lowerCost)

    for lowerCount in range(searchLimit + 1):
        partial = lowerCount * lowerCost

        if partial > best + 1e-9:
            break

        higherCount = max(0, math.ceil((low - partial - 1e-12) / higherCost))
        candidate = partial + higherCount * higherCost

        if candidate < best and capacity(candidate, lowerCost, higherCost, size) >= size:
            best = candidate

    return best


def fibonacciValues(limit):
    values = [0, 1, 1]

    for _ in range(3, limit + 1):
        values.append(values[-1] + values[-2])

    return values


def guessingGameSum():
    fibonacci = fibonacciValues(TERMS)
    total = 0.0

    for k in range(1, TERMS + 1):
        total += optimalCost(LIMIT, math.sqrt(k), math.sqrt(fibonacci[k]))

    return format(total, ".8f")


def runTests():
    assert round(optimalCost(5, 2, 3), 8) == 5
    assert format(optimalCost(500, math.sqrt(2), math.sqrt(3)), ".8f") == "13.22073197"
    assert round(optimalCost(20_000, 5, 7), 8) == 82
    assert format(optimalCost(2_000_000, math.sqrt(5), math.sqrt(7)), ".8f") == "49.63755955"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = guessingGameSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
