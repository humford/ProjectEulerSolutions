from decimal import Decimal, ROUND_HALF_UP, getcontext
import math
import time


def expectedTimeFloat(firstDepth):
    if firstDepth <= 0:
        return float("inf")

    previous = 0.0
    current = firstDepth
    total = firstDepth + 1.0

    for _ in range(10000):
        term = math.exp(-current)
        total += term
        if term < 1e-16:
            break

        increment = current - previous
        if increment > 80:
            break

        nextDepth = math.exp(increment)
        if nextDepth <= current:
            return float("inf")

        previous, current = current, nextDepth

    return total


def expectedTimeDecimal(firstDepth, epsilon):
    if firstDepth <= 0:
        return Decimal("Infinity")

    previous = Decimal(0)
    current = firstDepth
    total = firstDepth + Decimal(1)

    for _ in range(20000):
        term = (-current).exp()
        total += term
        if term < epsilon:
            break

        increment = current - previous
        if increment > Decimal(80):
            break

        nextDepth = increment.exp()
        if nextDepth <= current:
            return Decimal("Infinity")

        previous, current = current, nextDepth

    return total


def coarseBracket():
    bestDepth = 0.1
    bestValue = float("inf")
    depth = 0.0001

    while depth <= 3.0:
        value = expectedTimeFloat(depth)
        if value < bestValue:
            bestDepth = depth
            bestValue = value
        depth += 0.0005

    def finite(depth):
        return math.isfinite(expectedTimeFloat(depth))

    width = 0.05
    while width > 0.002:
        left = max(0.0001, bestDepth - width)
        right = min(3.0, bestDepth + width)
        middle = (left + right) / 2
        q1 = left + (right - left) / 4
        q3 = left + 3 * (right - left) / 4

        if all(finite(depth) for depth in (left, q1, middle, q3, right)):
            if (
                expectedTimeFloat(middle) <= expectedTimeFloat(left)
                and expectedTimeFloat(middle) <= expectedTimeFloat(right)
            ):
                return left, right

        width *= 0.6

    return max(0.0001, bestDepth - 0.005), min(3.0, bestDepth + 0.005)


def goldenSectionMinimum(left, right, iterations, epsilon):
    sqrt5 = Decimal(5).sqrt()
    phi = (Decimal(1) + sqrt5) / 2
    inversePhi = Decimal(1) / phi

    c = right - (right - left) * inversePhi
    d = left + (right - left) * inversePhi
    fc = expectedTimeDecimal(c, epsilon)
    fd = expectedTimeDecimal(d, epsilon)

    for _ in range(iterations):
        if fc < fd:
            right, d, fd = d, c, fc
            c = right - (right - left) * inversePhi
            fc = expectedTimeDecimal(c, epsilon)
        else:
            left, c, fc = c, d, fd
            d = left + (right - left) * inversePhi
            fd = expectedTimeDecimal(d, epsilon)

    depth = (left + right) / 2
    return depth, expectedTimeDecimal(depth, epsilon)


def solveDecimal():
    getcontext().prec = 120
    leftFloat, rightFloat = coarseBracket()
    _, value = goldenSectionMinimum(
        Decimal(str(leftFloat)),
        Decimal(str(rightFloat)),
        250,
        Decimal("1e-90"),
    )
    return value


def solve():
    return str(solveDecimal().quantize(Decimal("1e-9"), rounding=ROUND_HALF_UP))


def runTests():
    assert expectedTimeFloat(0.1) > 0
    assert solve() == "2.364497769"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
