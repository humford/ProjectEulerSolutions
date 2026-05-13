from math import gcd
import time


def addMultiplier(coefficients, multiplier, limit):
    updates = {multiplier: 1}
    for lcmValue, coefficient in list(coefficients.items()):
        combined = lcmValue * multiplier // gcd(lcmValue, multiplier)
        if combined <= limit:
            updates[combined] = updates.get(combined, 0) - coefficient

    for lcmValue, coefficient in updates.items():
        updated = coefficients.get(lcmValue, 0) + coefficient
        if updated:
            coefficients[lcmValue] = updated
        elif lcmValue in coefficients:
            del coefficients[lcmValue]


def intervalUnionCount(coefficients, low, high):
    total = 0
    for lcmValue, coefficient in coefficients.items():
        total += coefficient * (high // lcmValue - low // lcmValue)
    return total


def multiplicationTableCount(m, n):
    m, n = sorted((m, n))
    total = n
    coefficients = {}
    limit = m * n

    for minimumMultiplier in range(m, 1, -1):
        addMultiplier(coefficients, minimumMultiplier, limit)
        low = (minimumMultiplier - 1) * n
        high = minimumMultiplier * n
        total += intervalUnionCount(coefficients, low, high)

    return total


def runTests():
    assert multiplicationTableCount(3, 4) == 8
    assert multiplicationTableCount(64, 64) == 1263
    assert multiplicationTableCount(12, 345) == 1998
    assert multiplicationTableCount(32, 10 ** 15) == 13_826_382_602_124_302


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = multiplicationTableCount(64, 10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
