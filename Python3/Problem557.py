import math
import time


def triangleCuttingQuadruples(limit):
    for areaA in range(1, limit - 2):
        areaASquared = areaA * areaA

        # Let h = 2a + b + c + d.  From area ratios,
        # bc(2a + b + c + d) = a^2 d.
        for h in range(2 * areaA + 3, limit + areaA + 1):
            common = math.gcd(h, areaASquared)
            dStep = h // common
            maxMultiplier = (h - 2 * areaA - 2) // dStep
            if maxMultiplier <= 0:
                continue

            productStep = areaASquared // common
            areaD = dStep
            productBC = productStep
            for _ in range(maxMultiplier):
                sumBC = h - 2 * areaA - areaD
                discriminant = sumBC * sumBC - 4 * productBC

                if discriminant >= 0:
                    root = math.isqrt(discriminant)
                    if root * root == discriminant and (sumBC - root) % 2 == 0:
                        areaB = (sumBC - root) // 2
                        areaC = (sumBC + root) // 2
                        if areaB > 0 and areaB <= areaC:
                            yield areaA, areaB, areaC, areaD

                areaD += dStep
                productBC += productStep


def triangleCuttingSum(limit):
    return sum(sum(quadruple) for quadruple in triangleCuttingQuadruples(limit))


def runTests():
    assert triangleCuttingSum(20) == 259
    total55 = sorted(
        quadruple
        for quadruple in triangleCuttingQuadruples(55)
        if sum(quadruple) == 55
    )
    assert total55 == [(20, 2, 24, 9), (22, 8, 11, 14)]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangleCuttingSum(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
