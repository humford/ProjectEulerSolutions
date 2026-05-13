import math
import time
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


def lcm(a, b):
    return a // math.gcd(a, b) * b


def searchBestSum(maxN, targetN):
    denominator = 1
    for n in range(1, maxN + 1):
        denominator = lcm(denominator, n)

    scale = [0] * (maxN + 1)
    for n in range(1, maxN + 1):
        scale[n] = denominator // n

    lower = [0] * (maxN + 1)
    upper = [denominator] * (maxN + 1)
    order = [1]
    best = None
    reachesMax = False

    def recurse(n, order, lower, upper, lowerSum):
        nonlocal best, reachesMax

        if n == targetN:
            if best is None or lowerSum < best:
                best = lowerSum

        if n == maxN:
            reachesMax = True
            return

        m = n + 1
        step = scale[m]
        for position in range(m):
            newOrder = order[:position] + [m] + order[position:]
            newLower = lower[:]
            newUpper = upper[:]
            newLowerSum = lowerSum
            feasible = True

            for rank, point in enumerate(newOrder):
                lb = rank * step
                ub = (rank + 1) * step

                if lb > newLower[point]:
                    newLowerSum += lb - newLower[point]
                    newLower[point] = lb
                if ub < newUpper[point]:
                    newUpper[point] = ub

                if newLower[point] >= newUpper[point]:
                    feasible = False
                    break

            if feasible:
                recurse(m, newOrder, newLower, newUpper, newLowerSum)

    recurse(1, order, lower, upper, 0)
    return best, denominator, reachesMax


def formatScaled(value, denominator, places=12):
    getcontext().prec = 80
    decimal = Decimal(value) / Decimal(denominator)
    quantizer = Decimal(1).scaleb(-places)
    return str(decimal.quantize(quantizer, rounding=ROUND_HALF_UP))


def F(n):
    best, denominator, _ = searchBestSum(n, n)
    return Fraction(best, denominator)


def runTests():
    assert F(4) == Fraction(3, 2)
    best17, denominator, reaches18 = searchBestSum(18, 17)
    assert best17 is not None
    assert not reaches18
    assert formatScaled(best17, denominator, 12) == "8.146681749623"


if __name__ == "__main__":
    runTests()
    start = time.time()
    best, denominator, _ = searchBestSum(18, 17)
    answer = formatScaled(best, denominator, 12)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
