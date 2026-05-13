import functools
import math
import time


MODULUS = 135_707_531
PROBLEM_M = 12_345
PROBLEM_N = 6_789


def powerSum(limit, exponent):
    if limit <= 0:
        return 0
    if exponent == 0:
        return limit
    if exponent == 1:
        return limit * (limit + 1) // 2
    if exponent == 2:
        return limit * (limit + 1) * (2 * limit + 1) // 6
    if exponent == 3:
        return limit**2 * (limit + 1) ** 2 // 4
    if exponent == 4:
        return (
            limit
            * (limit + 1)
            * (2 * limit + 1)
            * (3 * limit**2 + 3 * limit - 1)
            // 30
        )
    raise ValueError("unsupported exponent")


def quadrilateralCount(m, n):
    if m < 0 or n < 0:
        raise ValueError("grid dimensions must be non-negative")
    if m == 0 or n == 0:
        return 0

    pointCount = (m + 1) * (n + 1)

    @functools.lru_cache(maxsize=None)
    def coprimeMomentSum(width, height, xPower, yPower):
        if width <= 0 or height <= 0:
            return 0

        root = math.isqrt(width)
        upper = min(height, width // root)
        total = powerSum(width, xPower) * powerSum(height, yPower)

        for divisor in range(2, upper + 1):
            total -= (
                coprimeMomentSum(width // divisor, height // divisor, xPower, yPower)
                * divisor ** (xPower + yPower)
            )

        for quotient in range(1, root):
            lowHeight = height // (width // (quotient + 1) + 1)
            highHeight = height // (width // quotient)

            if lowHeight == highHeight:
                total -= coprimeMomentSum(quotient, lowHeight, xPower, yPower) * (
                    powerSum(width // quotient, xPower + yPower)
                    - powerSum(width // (quotient + 1), xPower + yPower)
                )
            else:
                low = max(width // (quotient + 1), height // (lowHeight + 1))
                high = min(width // quotient, height // lowHeight)
                if high > low:
                    total -= coprimeMomentSum(
                        quotient, lowHeight, xPower, yPower
                    ) * (
                        powerSum(high, xPower + yPower)
                        - powerSum(low, xPower + yPower)
                    )

                if highHeight:
                    low = max(width // (quotient + 1), height // (highHeight + 1))
                    high = min(width // quotient, height // highHeight)
                    if high > low:
                        total -= coprimeMomentSum(
                            quotient, highHeight, xPower, yPower
                        ) * (
                            powerSum(high, xPower + yPower)
                            - powerSum(low, xPower + yPower)
                        )

        return total

    def positiveMomentSum(xPower, yPower, gcdPower):
        if gcdPower == 0:
            return powerSum(m, xPower) * powerSum(n, yPower)

        root = math.isqrt(m)
        upper = min(n, m // root)
        total = 0

        for divisor in range(1, upper + 1):
            total += (
                coprimeMomentSum(m // divisor, n // divisor, xPower, yPower)
                * divisor ** (xPower + yPower + gcdPower)
            )

        for quotient in range(1, root):
            lowHeight = n // (m // (quotient + 1) + 1)
            highHeight = n // (m // quotient)

            if lowHeight == highHeight:
                total += coprimeMomentSum(quotient, lowHeight, xPower, yPower) * (
                    powerSum(m // quotient, xPower + yPower + gcdPower)
                    - powerSum(m // (quotient + 1), xPower + yPower + gcdPower)
                )
            else:
                low = max(m // (quotient + 1), n // (lowHeight + 1))
                high = min(m // quotient, n // lowHeight)
                if high > low:
                    total += coprimeMomentSum(
                        quotient, lowHeight, xPower, yPower
                    ) * (
                        powerSum(high, xPower + yPower + gcdPower)
                        - powerSum(low, xPower + yPower + gcdPower)
                    )

                if highHeight:
                    low = max(m // (quotient + 1), n // (highHeight + 1))
                    high = min(m // quotient, n // highHeight)
                    if high > low:
                        total += coprimeMomentSum(
                            quotient, highHeight, xPower, yPower
                        ) * (
                            powerSum(high, xPower + yPower + gcdPower)
                            - powerSum(low, xPower + yPower + gcdPower)
                        )

        return total

    def gridMomentSum(xPower, yPower, gcdPower):
        total = positiveMomentSum(xPower, yPower, gcdPower)
        if xPower == 0:
            total += powerSum(n, yPower + gcdPower)
        if yPower == 0:
            total += powerSum(m, xPower + gcdPower)
        if xPower + yPower + gcdPower == 0:
            total += 1
        return total

    requiredMoments = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 0, 2),
        (0, 1, 0),
        (0, 1, 1),
        (0, 1, 2),
        (0, 2, 0),
        (0, 3, 0),
        (1, 0, 0),
        (1, 0, 1),
        (1, 0, 2),
        (1, 1, 0),
        (1, 1, 1),
        (1, 1, 2),
        (1, 2, 0),
        (1, 3, 0),
        (2, 0, 0),
        (2, 1, 0),
        (2, 2, 0),
        (2, 3, 0),
        (3, 0, 0),
        (3, 1, 0),
        (3, 2, 0),
        (3, 3, 0),
    ]
    moment = {key: gridMomentSum(*key) for key in requiredMoments}

    s000 = moment[(0, 0, 0)]
    s001 = moment[(0, 0, 1)]
    s002 = moment[(0, 0, 2)]
    s010 = moment[(0, 1, 0)]
    s011 = moment[(0, 1, 1)]
    s012 = moment[(0, 1, 2)]
    s020 = moment[(0, 2, 0)]
    s030 = moment[(0, 3, 0)]
    s100 = moment[(1, 0, 0)]
    s101 = moment[(1, 0, 1)]
    s102 = moment[(1, 0, 2)]
    s110 = moment[(1, 1, 0)]
    s111 = moment[(1, 1, 1)]
    s112 = moment[(1, 1, 2)]
    s120 = moment[(1, 2, 0)]
    s130 = moment[(1, 3, 0)]
    s200 = moment[(2, 0, 0)]
    s210 = moment[(2, 1, 0)]
    s220 = moment[(2, 2, 0)]
    s230 = moment[(2, 3, 0)]
    s300 = moment[(3, 0, 0)]
    s310 = moment[(3, 1, 0)]
    s320 = moment[(3, 2, 0)]
    s330 = moment[(3, 3, 0)]

    # This combination is 6 times the sum of all non-degenerate triangle areas.
    areaSumTimesSix = (
        (s012 - 11 * s230 - s210 - s030) * (m + 1)
        + (s102 - 11 * s320 - s300 - s120) * (n + 1)
        - (s112 - 11 * s330 - s310 - s130)
        - (s002 - 11 * s220 - s200 - s020) * (m + 1) * (n + 1)
    )

    collinearTriples = (
        2
        * (
            (s010 - s011) * (m + 1)
            + (s100 - s101) * (n + 1)
            - (s000 - s001) * (m + 1) * (n + 1)
            - (s110 - s111)
        )
        + s020
        - (n + 2) * s010
        + (n + 1) * s000
        + s200
        - (m + 2) * s100
        + (m + 1) * s000
    )

    collinearQuadruplesTimesTwo = (
        (4 * s000 - 6 * s001 + 2 * s002) * (m + 1) * (n + 1)
        + 4 * s110
        - 6 * s111
        + 2 * s112
        - (4 * s100 - 6 * s101 + 2 * s102) * (n + 1)
        - (4 * s010 - 6 * s011 + 2 * s012) * (m + 1)
        + s030
        - (n + 4) * s020
        + (3 * n + 5) * s010
        - 2 * (n + 1) * s000
        + s300
        - (m + 4) * s200
        + (3 * m + 5) * s100
        - 2 * (m + 1) * s000
    )

    return (
        math.comb(pointCount, 4)
        - math.comb(pointCount, 3)
        + areaSumTimesSix // 3
        + (7 - 2 * pointCount) * collinearTriples
        + 7 * (collinearQuadruplesTimesTwo // 2)
    )


def runTests():
    assert quadrilateralCount(1, 1) == 1
    assert quadrilateralCount(2, 2) == 94
    assert quadrilateralCount(3, 7) == 39_590
    assert quadrilateralCount(12, 3) == 309_000
    assert quadrilateralCount(123, 45) == 70_542_215_894_646


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = quadrilateralCount(PROBLEM_M, PROBLEM_N) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
