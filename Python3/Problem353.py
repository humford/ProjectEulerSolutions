import heapq
import math
import time
from collections import defaultdict
from functools import lru_cache


TARGET_EXPONENT = 15
EXACT_NODE_LIMIT = 1000
LOCAL_ANGLE_LIMITS = (0.04, 0.06, 0.08)


def primeFactorSieve(limit):
    smallestFactor = list(range(limit + 1))

    if limit >= 1:
        smallestFactor[1] = 1

    for number in range(2, math.isqrt(limit) + 1):
        if smallestFactor[number] != number:
            continue

        for multiple in range(number * number, limit + 1, number):
            if smallestFactor[multiple] == multiple:
                smallestFactor[multiple] = number

    return smallestFactor


def factorize(number, smallestFactor):
    factors = defaultdict(int)

    while number > 1:
        factor = smallestFactor[number]

        while number % factor == 0:
            factors[factor] += 1
            number //= factor

    return factors


def gaussianMultiply(first, second):
    real1, imag1 = first
    real2, imag2 = second

    return (
        real1 * real2 - imag1 * imag2,
        real1 * imag2 + imag1 * real2,
    )


def gaussianPower(value, exponent):
    result = (1, 0)
    base = value

    while exponent:
        if exponent & 1:
            result = gaussianMultiply(result, base)

        base = gaussianMultiply(base, base)
        exponent //= 2

    return result


@lru_cache(maxsize=None)
def primeSquareRepresentation(prime):
    for first in range(1, math.isqrt(prime) + 1):
        secondSquared = prime - first * first
        second = math.isqrt(secondSquared)

        if second * second == secondSquared:
            return first, second

    raise ValueError("No square representation found for prime " + str(prime))


def twoSquareRepresentations(factors):
    if not factors:
        return {(1, 0)}

    factors = dict(factors)
    representations = {(1, 0)}
    scale = 1
    twoExponent = factors.pop(2, 0)

    if twoExponent:
        scale *= 2 ** (twoExponent // 2)

        if twoExponent & 1:
            representations = {
                gaussianMultiply(representation, (1, 1))
                for representation in representations
            }

    for prime in list(factors):
        exponent = factors[prime]

        if prime % 4 != 3:
            continue

        if exponent & 1:
            return set()

        scale *= prime ** (exponent // 2)
        del factors[prime]

    for prime, exponent in sorted(factors.items()):
        if prime % 4 != 1:
            continue

        first, second = primeSquareRepresentation(prime)
        primeFactors = [
            gaussianMultiply(
                gaussianPower((first, second), count),
                gaussianPower((first, -second), exponent - count),
            )
            for count in range(exponent + 1)
        ]
        representations = {
            gaussianMultiply(representation, primeFactor)
            for representation in representations
            for primeFactor in primeFactors
        }

    normalized = set()
    for first, second in representations:
        first = abs(first) * scale
        second = abs(second) * scale

        if first < second:
            first, second = second, first

        normalized.add((first, second))

    return normalized


def stationOrbits(radius):
    smallestFactor = primeFactorSieve(2 * radius)
    orbits = set()

    for z in range(radius + 1):
        if z == radius:
            representations = {(0, 0)}
        else:
            factors = factorize(radius - z, smallestFactor)

            for prime, exponent in factorize(radius + z, smallestFactor).items():
                factors[prime] += exponent

            representations = twoSquareRepresentations(factors)

        for x, y in representations:
            orbits.add((x, y, z))

    return sorted(orbits, key=lambda point: (-point[2], -point[0], -point[1]))


def roadRiskFromDot(dotProduct, radiusSquared):
    cosine = max(-1.0, min(1.0, dotProduct / radiusSquared))
    angle = math.acos(cosine)

    return (angle / math.pi) ** 2


def bestSymmetricJourney(distances, points, radius):
    radiusSquared = radius * radius
    best = 1.0

    for distance, (x, y, z) in zip(distances, points):
        crossingRisk = roadRiskFromDot(x * x + y * y - z * z, radiusSquared)
        candidate = 2 * distance + crossingRisk

        if candidate < best:
            best = candidate

    return best


def exactMinimalRisk(radius, points):
    radiusSquared = radius * radius
    distances = [float("inf")] * len(points)
    distances[0] = 0.0
    queue = [(0.0, 0)]

    while queue:
        distance, index = heapq.heappop(queue)

        if distance != distances[index]:
            continue

        x, y, z = points[index]

        for nextIndex, (nextX, nextY, nextZ) in enumerate(points):
            if nextIndex == index:
                continue

            dotProduct = x * nextX + y * nextY + z * nextZ
            candidate = distance + roadRiskFromDot(dotProduct, radiusSquared)

            if candidate < distances[nextIndex]:
                distances[nextIndex] = candidate
                heapq.heappush(queue, (candidate, nextIndex))

    return bestSymmetricJourney(distances, points, radius)


def localMinimalRisk(radius, points, angleLimit):
    radiusSquared = radius * radius
    chordLimit = 2 * radius * math.sin(angleLimit / 2)
    chordLimitSquared = chordLimit * chordLimit
    cellSize = max(chordLimit, 1)
    grid = defaultdict(list)

    for index, point in enumerate(points):
        key = tuple(int(coordinate // cellSize) for coordinate in point)
        grid[key].append(index)

    offsets = [
        (dx, dy, dz)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
    ]
    neighbors = [[] for _point in points]

    for index, (x, y, z) in enumerate(points):
        key = tuple(int(coordinate // cellSize) for coordinate in (x, y, z))

        for dx, dy, dz in offsets:
            neighborKey = (key[0] + dx, key[1] + dy, key[2] + dz)

            for nextIndex in grid.get(neighborKey, ()):
                if nextIndex == index:
                    continue

                nextX, nextY, nextZ = points[nextIndex]
                dotProduct = x * nextX + y * nextY + z * nextZ
                chordSquared = 2 * radiusSquared - 2 * dotProduct

                if chordSquared <= chordLimitSquared:
                    neighbors[index].append(
                        (
                            nextIndex,
                            roadRiskFromDot(dotProduct, radiusSquared),
                        )
                    )

    distances = [float("inf")] * len(points)
    distances[0] = 0.0
    queue = [(0.0, 0)]

    while queue:
        distance, index = heapq.heappop(queue)

        if distance != distances[index]:
            continue

        for nextIndex, risk in neighbors[index]:
            candidate = distance + risk

            if candidate < distances[nextIndex]:
                distances[nextIndex] = candidate
                heapq.heappush(queue, (candidate, nextIndex))

    if any(distance == float("inf") for distance in distances):
        raise RuntimeError("Local graph is disconnected for radius " + str(radius))

    return bestSymmetricJourney(distances, points, radius)


def minimalRisk(radius):
    points = stationOrbits(radius)

    if len(points) <= EXACT_NODE_LIMIT:
        return exactMinimalRisk(radius, points)

    risks = [localMinimalRisk(radius, points, angle) for angle in LOCAL_ANGLE_LIMITS]

    if abs(risks[-1] - risks[-2]) > 1e-14:
        raise RuntimeError("Local graph answer did not stabilize for " + str(radius))

    return risks[-1]


def riskyMoonSum():
    total = sum(minimalRisk((1 << exponent) - 1) for exponent in range(1, 16))

    return f"{total:.10f}"


def runTests():
    assert round(minimalRisk(7), 10) == 0.1784943998

    points = stationOrbits(1023)
    exact = exactMinimalRisk(1023, points)
    local = localMinimalRisk(1023, points, 0.06)
    assert abs(exact - local) < 1e-14

    points = stationOrbits(4095)
    local = localMinimalRisk(4095, points, 0.04)
    widerLocal = localMinimalRisk(4095, points, 0.06)
    assert abs(local - widerLocal) < 1e-14


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = riskyMoonSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
