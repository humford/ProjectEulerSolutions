from math import isqrt
import time


TARGET_HIT = 70


def triangularNumber(index):
    return index * (index + 1) // 2


def factorization(value):
    factors = {}
    while value % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        value //= 2

    divisor = 3
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor += 2

    if value > 1:
        factors[value] = factors.get(value, 0) + 1

    return factors


def combineFactorizations(left, right):
    combined = dict(left)
    for prime, exponent in right.items():
        combined[prime] = combined.get(prime, 0) + exponent
    return combined


def divisorsFromFactors(items, index=0):
    if index == len(items):
        yield 1
        return

    prime, exponent = items[index]
    power = 1
    for _ in range(exponent + 1):
        for divisor in divisorsFromFactors(items, index + 1):
            yield power * divisor
        power *= prime


def nextTriangleState(triangleIndex):
    product = triangleIndex * (triangleIndex + 1)
    root = isqrt(product)
    factors = combineFactorizations(
        factorization(triangleIndex), factorization(triangleIndex + 1)
    )

    bestPair = None
    for left in divisorsFromFactors(list(factors.items())):
        if left > root:
            continue

        right = product // left
        if (left ^ right) & 1 == 0:
            continue
        if right - left <= 1:
            continue

        difference = right - left
        if bestPair is None or difference < bestPair[0]:
            bestPair = (difference, left, right)

    difference, left, right = bestPair
    step = (difference - 1) // 2
    nextIndex = (left + right - 1) // 2
    return nextIndex, step


def triangleHits(count):
    sequenceIndex = 0
    triangleIndex = 2
    hits = [(sequenceIndex, triangleIndex, triangularNumber(triangleIndex))]

    while len(hits) < count:
        triangleIndex, step = nextTriangleState(triangleIndex)
        sequenceIndex += step
        hits.append((sequenceIndex, triangleIndex, triangularNumber(triangleIndex)))

    return hits


def solve():
    return triangleHits(TARGET_HIT)[-1][0]


def runTests():
    expectedPrefix = [
        (0, 2, 3),
        (2, 3, 6),
        (7, 6, 21),
        (12, 8, 36),
    ]
    assert triangleHits(4) == expectedPrefix

    tenthIndex, tenthTriangleIndex, tenthValue = triangleHits(10)[-1]
    assert tenthIndex == 2_964
    assert tenthValue == 1_439_056
    assert triangularNumber(tenthTriangleIndex) == tenthValue


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
