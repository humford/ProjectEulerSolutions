from math import gcd, lcm
import time


TARGET = 12


def rationalCoordinates(limit):
    values = []
    for denominator in range(1, limit + 1):
        for numerator in range(-denominator + 1, denominator):
            if gcd(abs(numerator), denominator) == 1:
                values.append((numerator, denominator))
    return values


def buildPoints(limit):
    rationals = rationalCoordinates(limit)
    points = []

    for xNumerator, xDenominator in rationals:
        xDenominatorSquared = xDenominator * xDenominator
        for yNumerator, yDenominator in rationals:
            yDenominatorSquared = yDenominator * yDenominator
            if (
                xNumerator * xNumerator * yDenominatorSquared
                + yNumerator * yNumerator * xDenominatorSquared
                < xDenominatorSquared * yDenominatorSquared
            ):
                points.append((xNumerator, xDenominator, yNumerator, yDenominator))

    return points


def scaledComponents(left, right):
    x1Numerator, x1Denominator, y1Numerator, y1Denominator = left
    x2Numerator, x2Denominator, y2Numerator, y2Denominator = right

    firstDenominator = lcm(x1Denominator, y1Denominator)
    firstX = x1Numerator * (firstDenominator // x1Denominator)
    firstY = y1Numerator * (firstDenominator // y1Denominator)

    secondDenominator = lcm(x2Denominator, y2Denominator)
    secondX = x2Numerator * (secondDenominator // x2Denominator)
    secondY = y2Numerator * (secondDenominator // y2Denominator)

    denominator = lcm(firstDenominator, secondDenominator)
    firstScale = denominator // firstDenominator
    secondScale = denominator // secondDenominator

    return (
        firstX * firstScale,
        firstY * firstScale,
        secondX * secondScale,
        secondY * secondScale,
        denominator,
    )


def normalizedDirection(x, y):
    if x == 0 and y == 0:
        return (0, 0)

    divisor = gcd(abs(x), abs(y))
    x //= divisor
    y //= divisor

    if x < 0 or (x == 0 and y < 0):
        x = -x
        y = -y

    return (x, y)


def geodesicId(left, right):
    x1, y1, x2, y2, denominator = scaledComponents(left, right)
    crossProduct = x1 * y2 - y1 * x2

    if crossProduct == 0:
        if x1 == 0 and y1 == 0:
            direction = normalizedDirection(x2, y2)
        else:
            direction = normalizedDirection(x1, y1)
        return ("L", direction)

    radius1 = x1 * x1 + y1 * y1 + denominator * denominator
    radius2 = x2 * x2 + y2 * y2 + denominator * denominator

    centerXNumerator = radius1 * y2 - y1 * radius2
    centerYNumerator = x1 * radius2 - radius1 * x2
    centerDenominator = 2 * denominator * crossProduct

    if centerDenominator < 0:
        centerDenominator = -centerDenominator
        centerXNumerator = -centerXNumerator
        centerYNumerator = -centerYNumerator

    divisor = gcd(gcd(abs(centerXNumerator), abs(centerYNumerator)), centerDenominator)
    if divisor > 1:
        centerXNumerator //= divisor
        centerYNumerator //= divisor
        centerDenominator //= divisor

    return ("C", (centerXNumerator, centerYNumerator, centerDenominator))


def T(limit):
    points = buildPoints(limit)
    geodesics = {}

    for leftIndex, left in enumerate(points):
        for rightIndex in range(leftIndex + 1, len(points)):
            key = geodesicId(left, points[rightIndex])
            if key in geodesics:
                geodesics[key].add(leftIndex)
                geodesics[key].add(rightIndex)
            else:
                geodesics[key] = {leftIndex, rightIndex}

    total = 0
    for indices in geodesics.values():
        count = len(indices)
        if count >= 3:
            total += count * (count - 1) * (count - 2)

    return total


def solve():
    return T(TARGET)


def runTests():
    assert T(2) == 24
    assert T(3) == 1296


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
