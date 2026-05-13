import math
import time


def triangleArea(sideA, sideB, sideC):
    semiperimeter = (sideA + sideB + sideC) / 2
    squaredArea = (
        semiperimeter
        * (semiperimeter - sideA)
        * (semiperimeter - sideB)
        * (semiperimeter - sideC)
    )
    return math.sqrt(max(0, squaredArea))


def rotatePoints(points, angle):
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return [
        (cosine * x - sine * y, sine * x + cosine * y)
        for x, y in points
    ]


def minimumXAboveY(points, threshold):
    minimum = math.inf
    for index, (x1, y1) in enumerate(points):
        x2, y2 = points[(index + 1) % len(points)]
        if y1 >= threshold:
            minimum = min(minimum, x1)
        if y2 >= threshold:
            minimum = min(minimum, x2)

        dy = y2 - y1
        if dy == 0:
            continue
        ratio = (threshold - y1) / dy
        if 0 <= ratio <= 1:
            minimum = min(minimum, x1 + (x2 - x1) * ratio)
    return minimum


def buildUnitPentagon(diagonal):
    if not 0.5 < diagonal < 2:
        return None

    heightSquared = diagonal * diagonal - 0.25
    if heightSquared <= 0:
        return None

    apex = (0.5, math.sqrt(heightSquared))
    baseLeft = (0.0, 0.0)
    baseRight = (1.0, 0.0)

    halfChordSquared = 1 - (diagonal / 2) ** 2
    if halfChordSquared <= 0:
        return None

    midpoint = (
        (baseLeft[0] + apex[0]) / 2,
        (baseLeft[1] + apex[1]) / 2,
    )
    perpendicular = (
        -(apex[1] - baseLeft[1]) / diagonal,
        (apex[0] - baseLeft[0]) / diagonal,
    )
    offset = math.sqrt(halfChordSquared)
    leftShoulder = (
        midpoint[0] + offset * perpendicular[0],
        midpoint[1] + offset * perpendicular[1],
    )
    rightShoulder = (1 - leftShoulder[0], leftShoulder[1])
    return [baseLeft, leftShoulder, apex, rightShoulder, baseRight]


def unitPentagonArea(diagonal):
    return (
        2 * triangleArea(1, 1, diagonal)
        + triangleArea(diagonal, diagonal, 1)
    )


def precomputeRotations(points, angles):
    return [
        (
            rotatePoints(points, angle),
            min(y for _, y in rotatePoints(points, angle)),
            max(x for x, _ in rotatePoints(points, angle)),
        )
        for angle in angles
    ]


def cornerClearance(rotatedPoints, minimumY, maximumX, scale, epsilonY):
    threshold = minimumY + (1 + epsilonY) / scale
    minimumX = minimumXAboveY(rotatedPoints, threshold)
    if minimumX == math.inf:
        return math.inf
    return 1 + scale * (minimumX - maximumX)


def minimumClearance(points, precomputed, angles, scale, epsilonY):
    clearances = [
        cornerClearance(rotatedPoints, minimumY, maximumX, scale, epsilonY)
        for rotatedPoints, minimumY, maximumX in precomputed
    ]
    best = min(clearances)
    bestIndexes = sorted(
        range(len(angles)),
        key=lambda index: clearances[index],
    )[:3]

    goldenRatioConjugate = (math.sqrt(5) - 1) / 2

    def clearanceAt(angle):
        rotatedPoints = rotatePoints(points, angle)
        return cornerClearance(
            rotatedPoints,
            min(y for _, y in rotatedPoints),
            max(x for x, _ in rotatedPoints),
            scale,
            epsilonY,
        )

    for index in bestIndexes:
        left = angles[max(0, index - 1)]
        right = angles[min(len(angles) - 1, index + 1)]
        if right <= left:
            continue

        middleLeft = right - (right - left) * goldenRatioConjugate
        middleRight = left + (right - left) * goldenRatioConjugate
        valueLeft = clearanceAt(middleLeft)
        valueRight = clearanceAt(middleRight)

        for _ in range(22):
            if valueLeft < valueRight:
                right = middleRight
                middleRight = middleLeft
                valueRight = valueLeft
                middleLeft = right - (right - left) * goldenRatioConjugate
                valueLeft = clearanceAt(middleLeft)
            else:
                left = middleLeft
                middleLeft = middleRight
                valueLeft = valueRight
                middleRight = left + (right - left) * goldenRatioConjugate
                valueRight = clearanceAt(middleRight)
        best = min(best, valueLeft, valueRight)

    return best


def maximumScale(points, angleCount, bisectionIterations, epsilonY):
    angles = [
        (math.pi / 2) * index / (angleCount - 1)
        for index in range(angleCount)
    ]
    precomputed = precomputeRotations(points, angles)

    def feasible(scale):
        return minimumClearance(
            points,
            precomputed,
            angles,
            scale,
            epsilonY,
        ) >= -1e-13

    low = 0
    high = 2
    while feasible(high):
        high *= 1.3

    for _ in range(bisectionIterations):
        middle = (low + high) / 2
        if feasible(middle):
            low = middle
        else:
            high = middle
    return low


def scaledArea(diagonal, mode):
    points = buildUnitPentagon(diagonal)
    if points is None:
        return -1

    if mode == "coarse":
        scale = maximumScale(points, 450, 35, 1e-12)
    elif mode == "medium":
        scale = maximumScale(points, 1_400, 55, 1e-14)
    elif mode == "fine":
        scale = maximumScale(points, 8_000, 75, 1e-15)
    else:
        raise ValueError("unknown precision mode")

    return unitPentagonArea(diagonal) * scale * scale


def goldenMaximize(function, left, right, iterations):
    goldenRatioConjugate = (math.sqrt(5) - 1) / 2
    middleLeft = right - (right - left) * goldenRatioConjugate
    middleRight = left + (right - left) * goldenRatioConjugate
    valueLeft = function(middleLeft)
    valueRight = function(middleRight)

    for _ in range(iterations):
        if valueLeft > valueRight:
            right = middleRight
            middleRight = middleLeft
            valueRight = valueLeft
            middleLeft = right - (right - left) * goldenRatioConjugate
            valueLeft = function(middleLeft)
        else:
            left = middleLeft
            middleLeft = middleRight
            valueLeft = valueRight
            middleRight = left + (right - left) * goldenRatioConjugate
            valueRight = function(middleRight)

    if valueLeft > valueRight:
        return middleLeft, valueLeft
    return middleRight, valueRight


def largestPentagonalTableArea():
    bestDiagonal = None
    bestArea = -1
    for index in range(241):
        diagonal = 0.75 + 0.30 * index / 240
        area = scaledArea(diagonal, "coarse")
        if area > bestArea:
            bestArea = area
            bestDiagonal = diagonal

    cache = {}

    def mediumArea(diagonal):
        key = round(diagonal, 15)
        if key not in cache:
            cache[key] = scaledArea(diagonal, "medium")
        return cache[key]

    diagonal, _ = goldenMaximize(
        mediumArea,
        bestDiagonal - 0.02,
        bestDiagonal + 0.02,
        26,
    )
    diagonal, _ = goldenMaximize(
        mediumArea,
        diagonal - 0.002,
        diagonal + 0.002,
        35,
    )
    return format(scaledArea(diagonal, "fine"), ".10f")


def runTests():
    assert format(1.0, ".10f") == "1.0000000000"
    points = buildUnitPentagon(0.9)
    for index, (x1, y1) in enumerate(points):
        x2, y2 = points[(index + 1) % len(points)]
        assert abs(math.hypot(x2 - x1, y2 - y1) - 1) < 1e-9


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestPentagonalTableArea()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
