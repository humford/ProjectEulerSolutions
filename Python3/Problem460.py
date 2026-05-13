import math
import time


def fastestTimeValue(distance, window=30, radialEpsilon=0.5):
    half = distance // 2
    infinity = float("inf")
    best = [[infinity] * (half + 1) for _ in range(half + 1)]
    best[1][0] = 0.0

    logY = [0.0] + [math.log(y) for y in range(1, half + 1)]
    referenceX = [0] * (half + 1)
    for y in range(1, half + 1):
        referenceX[y] = half - math.isqrt(half * half - y * y)

    sourceRows = [[] for _ in range(half)]
    outerSquared = (half + radialEpsilon) * (half + radialEpsilon)
    innerRadius = max(0.0, half - radialEpsilon)
    innerSquared = innerRadius * innerRadius

    for x in range(half):
        dx = half - x
        dxSquared = dx * dx
        low = innerSquared - dxSquared
        high = outerSquared - dxSquared
        if high < 1:
            continue

        yLow = max(1, math.ceil(math.sqrt(max(0.0, low))))
        yHigh = min(half, math.floor(math.sqrt(max(0.0, high))))
        for y in range(yLow, yHigh + 1):
            radius = math.sqrt(dxSquared + y * y)
            if abs(radius - half) <= radialEpsilon + 1e-12:
                sourceRows[x].append(y)

    bestHalf = infinity
    for x0, rows in enumerate(sourceRows):
        for y0 in rows:
            base = best[y0][x0]
            if not math.isfinite(base):
                continue
            logY0 = logY[y0]
            for y in range(y0, half + 1):
                dy = y - y0
                inverseVelocity = 1.0 / y0 if dy == 0 else (logY[y] - logY0) / dy
                xRef = referenceX[y]
                xLow = max(x0, xRef - window)
                xHigh = min(half, xRef + 1)
                row = best[y]

                for x in range(xLow, xHigh + 1):
                    dx = x - x0
                    candidate = base + math.sqrt(dx * dx + dy * dy) * inverseVelocity
                    if candidate < row[x]:
                        row[x] = candidate
                        if x == half and candidate < bestHalf:
                            bestHalf = candidate

    return 2.0 * bestHalf


def fastestTime(distance):
    return format(fastestTimeValue(distance), ".9f")


def runTests():
    assert fastestTime(4) == "2.960516287"
    assert fastestTime(10) == "4.668187834"
    assert fastestTime(100) == "9.217221972"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fastestTime(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
