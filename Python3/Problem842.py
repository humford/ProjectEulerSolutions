from math import isqrt
import math
import time


MOD = 1_000_000_007


def inverseTriangular(count):
    discriminant = 1 + 8 * count
    root = isqrt(discriminant)
    if root * root != discriminant or (1 + root) % 2:
        raise ValueError("intersection count is not triangular")
    return (1 + root) // 2


def cyclesUsingAtLeastTwoEdges(n, matchingSize, factorials):
    if matchingSize < 2:
        return 0

    totalCycles = factorials[n - 1] // 2

    def cyclesContaining(k):
        if k == 0:
            return totalCycles
        return (1 << (k - 1)) * factorials[n - k - 1]

    none = 0
    for k in range(matchingSize + 1):
        term = math.comb(matchingSize, k) * cyclesContaining(k)
        none += term if k % 2 == 0 else -term

    exactlyOne = 0
    for k in range(1, matchingSize + 1):
        term = k * math.comb(matchingSize, k) * cyclesContaining(k)
        exactlyOne += term if (k - 1) % 2 == 0 else -term

    return totalCycles - none - exactlyOne


def pointMultiplicityDistribution(n):
    fullTurn = 2.0 * math.pi
    xs = [math.cos(fullTurn * k / n) for k in range(n)]
    ys = [math.sin(fullTurn * k / n) for k in range(n)]
    scale = 10**11
    counts = {}

    for a in range(n - 3):
        x1 = xs[a]
        y1 = ys[a]
        for b in range(a + 1, n - 2):
            x3 = xs[b]
            y3 = ys[b]
            abx = x3 - x1
            aby = y3 - y1
            for c in range(b + 1, n - 1):
                x2 = xs[c]
                y2 = ys[c]
                dx12 = x2 - x1
                dy12 = y2 - y1
                for d in range(c + 1, n):
                    x4 = xs[d]
                    y4 = ys[d]
                    dx34 = x4 - x3
                    dy34 = y4 - y3

                    denominator = dx12 * dy34 - dy12 * dx34
                    if abs(denominator) < 1e-18:
                        continue

                    t = (abx * dy34 - aby * dx34) / denominator
                    x = x1 + t * dx12
                    y = y1 + t * dy12
                    key = (int(round(x * scale)), int(round(y * scale)))
                    counts[key] = counts.get(key, 0) + 1

    distribution = {}
    try:
        for count in counts.values():
            multiplicity = inverseTriangular(count)
            distribution[multiplicity] = distribution.get(multiplicity, 0) + 1
        return distribution
    except ValueError:
        return clusteredPointMultiplicityDistribution(n, xs, ys)


def clusteredPointMultiplicityDistribution(n, xs, ys):
    cellSize = 1e-6
    epsilonSquared = (1e-9) ** 2
    grid = {}
    representativeXs = []
    representativeYs = []
    representativeCounts = []

    def addPoint(x, y):
        ix = int(math.floor(x / cellSize))
        iy = int(math.floor(y / cellSize))

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nearby = grid.get((ix + dx, iy + dy))
                if nearby is None:
                    continue
                for index in nearby:
                    xDiff = x - representativeXs[index]
                    yDiff = y - representativeYs[index]
                    if xDiff * xDiff + yDiff * yDiff <= epsilonSquared:
                        representativeCounts[index] += 1
                        return

        index = len(representativeCounts)
        representativeXs.append(x)
        representativeYs.append(y)
        representativeCounts.append(1)
        grid.setdefault((ix, iy), []).append(index)

    for a in range(n - 3):
        x1 = xs[a]
        y1 = ys[a]
        for b in range(a + 1, n - 2):
            x3 = xs[b]
            y3 = ys[b]
            abx = x3 - x1
            aby = y3 - y1
            for c in range(b + 1, n - 1):
                x2 = xs[c]
                y2 = ys[c]
                dx12 = x2 - x1
                dy12 = y2 - y1
                for d in range(c + 1, n):
                    x4 = xs[d]
                    y4 = ys[d]
                    dx34 = x4 - x3
                    dy34 = y4 - y3

                    denominator = dx12 * dy34 - dy12 * dx34
                    if abs(denominator) < 1e-18:
                        continue

                    t = (abx * dy34 - aby * dx34) / denominator
                    addPoint(x1 + t * dx12, y1 + t * dy12)

    distribution = {}
    for count in representativeCounts:
        multiplicity = inverseTriangular(count)
        distribution[multiplicity] = distribution.get(multiplicity, 0) + 1

    return distribution


def T(n, factorials):
    if n < 4:
        return 0

    distribution = pointMultiplicityDistribution(n)
    total = 0

    for multiplicity, pointCount in distribution.items():
        total += pointCount * cyclesUsingAtLeastTwoEdges(n, multiplicity, factorials)

    return total


def factorialsUpTo(limit):
    factorials = [1] * (limit + 1)
    for n in range(1, limit + 1):
        factorials[n] = factorials[n - 1] * n
    return factorials


def solve():
    factorials = factorialsUpTo(60)
    total = 0

    for n in range(3, 61):
        total = (total + T(n, factorials)) % MOD

    return total


def runTests():
    factorials = factorialsUpTo(8)
    assert T(5, factorials) == 20
    assert T(8, factorials) == 14_640


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
