import math
import time


LIMIT = 10**12
MODULUS = 10**8


def latticePointCount(a, b):
    discriminant = a * a + 4 * b

    if discriminant < 0:
        return 0

    root = math.isqrt(discriminant)

    if root * root != discriminant:
        return 0

    minimumNumerator = a - root
    maximumNumerator = a + root
    minimumX = (minimumNumerator + 1) // 2 if minimumNumerator % 2 else minimumNumerator // 2
    maximumX = maximumNumerator // 2
    total = 0

    for x in range(minimumX, maximumX + 1):
        total += a * x + b - x * x + 1

    return total


def bruteS(limit):
    total = 0

    for a in range(-limit, limit + 1):
        for b in range(-limit, limit + 1):
            total += latticePointCount(a, b)

    return total


def ceilDiv(numerator, denominator):
    return -((-numerator) // denominator)


def distanceContribution(distance):
    return (distance**3 + 5 * distance + 6) // 6


def contributionPrefix(distance):
    if distance < 0:
        return 0

    linearSum = distance * (distance + 1) // 2
    cubeSum = linearSum * linearSum
    return (cubeSum + 5 * linearSum) // 6 + distance + 1


def positiveRootLimit(distance, limit):
    value = (math.isqrt(distance * distance + 4 * limit) - distance) // 2

    while (value + 1) * (distance + value + 1) <= limit:
        value += 1

    while value * (distance + value) > limit:
        value -= 1

    return value


def smallDistanceCount(distance, limit):
    if distance == 0:
        return 2 * min(limit // 2, math.isqrt(limit)) + 1

    outsideLimit = positiveRootLimit(distance, limit)
    low = ceilDiv(-limit - distance, 2)
    high = (limit - distance) // 2
    intervals = [
        (-distance - outsideLimit, -distance),
        (-distance, 0),
        (0, outsideLimit),
    ]
    merged = []

    for start, end in intervals:
        start = max(start, low)
        end = min(end, high)

        if start > end:
            continue

        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return sum(end - start + 1 for start, end in merged)


def prefixRange(start, end, modulus):
    if end < start:
        return 0

    return (contributionPrefix(end) - contributionPrefix(start - 1)) % modulus


def largeSModulo(limit=LIMIT, modulus=MODULUS):
    split = math.isqrt(4 * limit)
    total = 0

    for distance in range(split + 1):
        total = (
            total
            + smallDistanceCount(distance, limit) * distanceContribution(distance)
        ) % modulus

    base = prefixRange(split + 1, limit, modulus)
    nearRootSum = base
    height = 1

    while True:
        upper = min(limit // height + height, limit + 2 * height)

        if upper <= split:
            break

        nearRootSum = (nearRootSum + prefixRange(split + 1, upper, modulus)) % modulus
        height += 1

    outsideSum = base
    outside = 1

    while True:
        upper = min(limit // outside - outside, limit - 2 * outside)

        if upper <= split:
            break

        outsideSum = (outsideSum + prefixRange(split + 1, upper, modulus)) % modulus
        outside += 1

    total = (total + 2 * nearRootSum + 2 * outsideSum - 2 * base) % modulus
    return total


def runTests():
    assert latticePointCount(1, 2) == 8
    assert latticePointCount(2, -1) == 1
    assert bruteS(5) == 344
    assert bruteS(100) == 26709528
    assert largeSModulo(5) == 344
    assert largeSModulo(100) == 26709528


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largeSModulo()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
