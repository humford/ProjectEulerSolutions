import math
import time


MOD = 1_000_000_007


def cubeRootFloor(value):
    low, high = 0, 1
    while high ** 3 <= value:
        high *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        if mid ** 3 <= value:
            low = mid
        else:
            high = mid
    return low


def turnCount(m):
    if m <= 1:
        return 0
    return math.isqrt(4 * m - 1) - 1


def turnCountPrefix(limit):
    if limit <= 1:
        return 0
    root = math.isqrt(limit)
    base = (root - 1) * root * (8 * root - 1) // 6
    square = root * root
    if limit == square:
        return base

    evenEnd = min(limit, square + root)
    evenCount = evenEnd - square
    partial = evenCount * (2 * root - 1)

    if limit > square + root:
        oddCount = limit - (square + root)
        partial += oddCount * (2 * root)

    return base + partial


def minimumSurfaceArea(cubes):
    if cubes == 1:
        return 6

    k = cubeRootFloor(cubes - 1)
    added = cubes - k ** 3
    firstLayer = k * k
    secondLayer = k * (k + 1)

    if added > firstLayer + secondLayer:
        layerStartBonus = 12
    elif added > firstLayer:
        layerStartBonus = 8
    else:
        layerStartBonus = 4

    p = min(added, firstLayer)
    q = min(max(added - p, 0), secondLayer)
    r = min(max(added - p - q, 0), (k + 1) ** 2)
    return 6 * k * k + layerStartBonus + 2 * (turnCount(p) + turnCount(q) + turnCount(r))


def g(cubes):
    return 6 * cubes - minimumSurfaceArea(cubes)


def sumMinimumSurfaceArea(limit, modulus=MOD):
    if limit <= 0:
        return 0
    total = 6
    if limit == 1:
        return total

    maxK = cubeRootFloor(limit - 1)
    for k in range(1, maxK + 1):
        start = k ** 3 + 1
        if start > limit:
            break
        blockLength = min(limit - k ** 3, (k + 1) ** 3 - k ** 3)

        firstLayer = k * k
        secondLayer = k * (k + 1)

        lenA = min(blockLength, firstLayer)
        remaining = blockLength - lenA
        lenB = min(remaining, secondLayer) if remaining > 0 else 0
        remaining -= lenB
        lenC = remaining if remaining > 0 else 0

        cFirst = turnCount(firstLayer)
        cSecond = turnCount(secondLayer)

        sumTurns = turnCountPrefix(lenA)
        if lenB:
            sumTurns += lenB * cFirst + turnCountPrefix(lenB)
        if lenC:
            sumTurns += lenC * (cFirst + cSecond) + turnCountPrefix(lenC)

        bonus = 4 * lenA + 8 * lenB + 12 * lenC
        total = (total + blockLength * (6 * k * k) + bonus + 2 * sumTurns) % modulus

    return total % modulus


def G(limit):
    totalIndividualSurface = 3 * (limit % MOD) * ((limit + 1) % MOD) % MOD
    return (totalIndividualSurface - sumMinimumSurfaceArea(limit)) % MOD


def runTests():
    assert g(10) == 30
    assert g(18) == 66
    assert G(18) == 530
    assert G(10 ** 6) == 951_640_919


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = G(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
