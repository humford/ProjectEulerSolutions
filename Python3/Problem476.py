from array import array
import math
import time


PROBLEM_LIMIT = 1_803


def triangleCount(limit):
    half = limit // 2
    return sum(
        sideA * (limit - 2 * sideA + 1)
        for sideA in range(1, half + 1)
    )


def inradiusSquaredAndHalfSines(a, b, c):
    semiperimeter = (a + b + c) / 2
    inradiusSquared = (
        (semiperimeter - a)
        * (semiperimeter - b)
        * (semiperimeter - c)
        / semiperimeter
    )
    sinHalfA = math.sqrt((semiperimeter - b) * (semiperimeter - c) / (b * c))
    sinHalfB = math.sqrt((semiperimeter - a) * (semiperimeter - c) / (a * c))
    return inradiusSquared, sinHalfA, sinHalfB


def maximumCircleArea(a, b, c):
    a, b, c = sorted((a, b, c))
    inradiusSquared, sinHalfA, sinHalfB = inradiusSquaredAndHalfSines(a, b, c)
    scaleA = (1 - sinHalfA) / (1 + sinHalfA)
    scaleASquared = scaleA * scaleA
    scaleB = (1 - sinHalfB) / (1 + sinHalfB)
    scaleBSquared = scaleB * scaleB

    if sinHalfB <= 2 * sinHalfA / (1 + sinHalfA * sinHalfA):
        areaFactor = 1 + scaleASquared + scaleBSquared
    else:
        areaFactor = 1 + scaleASquared + scaleASquared * scaleASquared

    return math.pi * inradiusSquared * areaFactor


def averageCirclePackingBrute(limit):
    total = 0.0
    count = 0
    for a in range(1, limit // 2 + 1):
        for b in range(a, limit - a + 1):
            if a + b > limit:
                break
            for c in range(b, a + b):
                total += maximumCircleArea(a, b, c)
                count += 1
    return total / count


def averageCirclePacking(limit):
    if limit < 2:
        return 0.0

    maxTableValue = 4 * limit * limit
    squareRoots = array("d", [0.0]) * (maxTableValue + 1)
    inverseSquareRoots = array("d", [0.0]) * (maxTableValue + 1)
    for value in range(1, maxTableValue + 1):
        root = math.sqrt(value)
        squareRoots[value] = root
        inverseSquareRoots[value] = 1.0 / root

    total = 0.0
    compensation = 0.0
    half = limit // 2

    for a in range(1, half + 1):
        twoA = 2 * a
        fourA = 4 * a
        for b in range(a, limit - a + 1):
            sideSum = a + b
            if sideSum > limit:
                break

            twoB = 2 * b
            fourB = 4 * b
            twoSideSum = 2 * sideSum
            for x in range(1, a + 1):
                c = sideSum - x
                termA = twoA - x
                termB = twoB - x
                inradiusSquared = (
                    x * termA * termB / (4.0 * (twoSideSum - x))
                )

                sinHalfA = (
                    squareRoots[x * termA] * inverseSquareRoots[fourB * c]
                )
                scaleA = (1.0 - sinHalfA) / (1.0 + sinHalfA)
                scaleASquared = scaleA * scaleA

                sinHalfB = (
                    squareRoots[x * termB] * inverseSquareRoots[fourA * c]
                )
                if sinHalfB <= 2.0 * sinHalfA / (1.0 + sinHalfA * sinHalfA):
                    scaleB = (1.0 - sinHalfB) / (1.0 + sinHalfB)
                    scaleBSquared = scaleB * scaleB
                    areaFactor = 1.0 + scaleASquared + scaleBSquared
                else:
                    areaFactor = (
                        1.0 + scaleASquared + scaleASquared * scaleASquared
                    )

                area = math.pi * inradiusSquared * areaFactor
                y = area - compensation
                updatedTotal = total + y
                compensation = (updatedTotal - total) - y
                total = updatedTotal

    return total / triangleCount(limit)


def runTests():
    assert round(maximumCircleArea(1, 1, 1), 5) == 0.31998
    assert round(averageCirclePackingBrute(2), 5) == 0.31998
    assert round(averageCirclePackingBrute(5), 5) == 1.25899
    assert round(averageCirclePacking(5), 5) == 1.25899


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = averageCirclePacking(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + format(answer, ".5f") + " in " + str(elapsed) + " seconds.")
