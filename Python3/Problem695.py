import math
import time


Y_ORDER_CODES = [
    (0, 1, 2),
    (2, 1, 0),
    (0, 2, 1),
    (2, 0, 1),
    (1, 2, 0),
    (1, 0, 2),
]


def gaussLegendreUnitInterval(count):
    nodes = [0.0] * count
    weights = [0.0] * count

    for rootIndex in range((count + 1) // 2):
        root = math.cos(math.pi * (rootIndex + 0.75) / (count + 0.5))

        for _ in range(100):
            previous = 1.0
            current = root
            for degree in range(2, count + 1):
                previous, current = (
                    current,
                    ((2 * degree - 1) * root * current - (degree - 1) * previous)
                    / degree,
                )
            derivative = count * (root * current - previous) / (root * root - 1.0)
            correction = current / derivative
            root -= correction
            if abs(correction) < 1e-16:
                break

        weight = 2.0 / ((1.0 - root * root) * derivative * derivative)
        left = (1.0 - root) / 2.0
        right = (1.0 + root) / 2.0
        mappedWeight = weight / 2.0
        nodes[rootIndex] = left
        nodes[count - 1 - rootIndex] = right
        weights[rootIndex] = mappedWeight
        weights[count - 1 - rootIndex] = mappedWeight

    return nodes, weights


def medianIndex(first, second, third):
    if (first <= second <= third) or (third <= second <= first):
        return 1
    if (second <= first <= third) or (third <= first <= second):
        return 0
    return 2


def integrateMedianLinear(firstScale, secondScale, thirdValue):
    breakpoints = [0.0, 1.0]

    if firstScale:
        point = thirdValue / firstScale
        if 0.0 < point < 1.0:
            breakpoints.append(point)

    if secondScale:
        point = 1.0 - thirdValue / secondScale
        if 0.0 < point < 1.0:
            breakpoints.append(point)

    if firstScale + secondScale:
        point = secondScale / (firstScale + secondScale)
        if 0.0 < point < 1.0:
            breakpoints.append(point)

    breakpoints = sorted(set(breakpoints))
    total = 0.0
    for left, right in zip(breakpoints, breakpoints[1:]):
        midpoint = (left + right) / 2.0
        first = firstScale * midpoint
        second = secondScale * (1.0 - midpoint)
        which = medianIndex(first, second, thirdValue)

        if which == 0:
            total += firstScale * (right * right - left * left) / 2.0
        elif which == 1:
            total += (
                secondScale * (right - left)
                - secondScale * (right * right - left * left) / 2.0
            )
        else:
            total += thirdValue * (right - left)

    return total


def secondLargestRectangleAreaExpectation(quadraturePoints=3000):
    nodes, weights = gaussLegendreUnitInterval(quadraturePoints)
    total = 0.0

    for yRatio, weight in zip(nodes, weights):
        lower = yRatio
        upper = 1.0 - yRatio
        permutationTotal = 0.0

        for firstCode, secondCode, thirdCode in Y_ORDER_CODES:
            firstScale = lower if firstCode == 0 else (upper if firstCode == 1 else 1.0)
            secondScale = lower if secondCode == 0 else (upper if secondCode == 1 else 1.0)
            thirdValue = lower if thirdCode == 0 else (upper if thirdCode == 1 else 1.0)
            permutationTotal += integrateMedianLinear(
                firstScale,
                secondScale,
                thirdValue,
            )

        total += weight * permutationTotal / 6.0

    return total / 4.0


def roundedSecondLargestRectangleAreaExpectation():
    return f"{secondLargestRectangleAreaExpectation():.10f}"


def runTests():
    assert abs(integrateMedianLinear(1.0, 1.0, 1.0) - 0.75) < 1e-15
    assert abs(integrateMedianLinear(1.0, 1.0, 0.0) - 0.25) < 1e-15
    _, weights = gaussLegendreUnitInterval(8)
    assert abs(sum(weights) - 1.0) < 1e-15


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedSecondLargestRectangleAreaExpectation()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
