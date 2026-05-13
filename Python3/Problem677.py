import time


MODULUS = 1_000_000_007
TARGET = 10_000
INVERSE_2 = (MODULUS + 1) // 2
INVERSE_6 = pow(6, MODULUS - 2, MODULUS)
INVERSE_24 = pow(24, MODULUS - 2, MODULUS)


def squareCoefficient(series, degree):
    if degree < 2:
        return 0

    half = degree // 2
    total = 0
    if degree % 2 == 0:
        total = series[half] * series[half]
        stop = half
    else:
        stop = half + 1

    for i in range(1, stop):
        total += 2 * series[i] * series[degree - i]

    return total % MODULUS


def setThreeCoefficient(series, squares, degree):
    if degree < 3:
        return 0

    cube = 0
    for i in range(1, degree):
        cube += series[i] * squares[degree - i]
    cube %= MODULUS

    mixed = 0
    for j in range(1, degree // 2 + 1):
        i = degree - 2 * j
        if i <= 0:
            break
        mixed += series[i] * series[j]
    mixed %= MODULUS

    total = cube + 3 * mixed
    if degree % 3 == 0:
        total += 2 * series[degree // 3]
    return total * INVERSE_6 % MODULUS


def setFourCoefficient(series, squares, degree):
    if degree < 4:
        return 0

    squareOfSquares = squareCoefficient(squares, degree)

    squareTimesDouble = 0
    for j in range(1, degree // 2 + 1):
        squareTimesDouble += squares[degree - 2 * j] * series[j]
    squareTimesDouble %= MODULUS

    doubleSquare = squares[degree // 2] if degree % 2 == 0 else 0

    timesTriple = 0
    for j in range(1, degree // 3 + 1):
        timesTriple += series[degree - 3 * j] * series[j]
    timesTriple %= MODULUS

    quadruple = series[degree // 4] if degree % 4 == 0 else 0

    return (
        squareOfSquares
        + 6 * squareTimesDouble
        + 3 * doubleSquare
        + 8 * timesTriple
        + 6 * quadruple
    ) * INVERSE_24 % MODULUS


def computePlanted(limit):
    red = [0] * (limit + 1)
    blue = [0] * (limit + 1)
    yellow = [0] * (limit + 1)
    allRoots = [0] * (limit + 1)
    nonYellowRoots = [0] * (limit + 1)
    allSquares = [0] * (limit + 1)
    nonYellowSquares = [0] * (limit + 1)

    for size in range(1, limit + 1):
        degree = size - 1
        allSquares[degree] = squareCoefficient(allRoots, degree)
        nonYellowSquares[degree] = squareCoefficient(nonYellowRoots, degree)

        totalSetTwo = allRoots[degree] + (1 if degree == 0 else 0)
        totalSetTwo += (
            allSquares[degree]
            + (allRoots[degree // 2] if degree % 2 == 0 else 0)
        ) * INVERSE_2
        totalSetTwo %= MODULUS

        nonYellowSetTwo = nonYellowRoots[degree] + (1 if degree == 0 else 0)
        nonYellowSetTwo += (
            nonYellowSquares[degree]
            + (nonYellowRoots[degree // 2] if degree % 2 == 0 else 0)
        ) * INVERSE_2
        nonYellowSetTwo %= MODULUS

        totalSetThree = (
            totalSetTwo
            + setThreeCoefficient(allRoots, allSquares, degree)
        ) % MODULUS

        red[size] = totalSetThree
        blue[size] = totalSetTwo
        yellow[size] = nonYellowSetTwo
        nonYellowRoots[size] = (red[size] + blue[size]) % MODULUS
        allRoots[size] = (nonYellowRoots[size] + yellow[size]) % MODULUS

    return red, blue, yellow, allRoots, nonYellowRoots, allSquares, nonYellowSquares


def nonYellowSetThreeAtDegree(degree, size, nonYellowRoots, nonYellowSquares, yellow):
    return (
        yellow[size]
        + setThreeCoefficient(nonYellowRoots, nonYellowSquares, degree)
    ) % MODULUS


def colouredGraphCount(nodes, plantedData=None):
    if plantedData is None:
        plantedData = computePlanted(nodes)

    red, blue, yellow, allRoots, nonYellowRoots, allSquares, nonYellowSquares = plantedData
    degree = nodes - 1

    totalSetThree = red[nodes]
    totalSetFour = (
        totalSetThree
        + setFourCoefficient(allRoots, allSquares, degree)
    ) % MODULUS
    nonYellowSetThree = nonYellowSetThreeAtDegree(
        degree,
        nodes,
        nonYellowRoots,
        nonYellowSquares,
        yellow,
    )

    vertexRooted = (totalSetFour + totalSetThree + nonYellowSetThree) % MODULUS

    allSquare = allSquares[nodes]
    if nodes == len(allSquares) - 1:
        allSquare = squareCoefficient(allRoots, nodes)
    yellowSquare = squareCoefficient(yellow, nodes)

    allDouble = allRoots[nodes // 2] if nodes % 2 == 0 else 0
    yellowDouble = yellow[nodes // 2] if nodes % 2 == 0 else 0

    directedEdgeRooted = (allSquare - yellowSquare) % MODULUS
    edgeRooted = (
        allSquare + allDouble - yellowSquare - yellowDouble
    ) * INVERSE_2 % MODULUS

    return (vertexRooted + edgeRooted - directedEdgeRooted) % MODULUS


def runTests(plantedData):
    assert colouredGraphCount(2, plantedData) == 5
    assert colouredGraphCount(3, plantedData) == 15
    assert colouredGraphCount(4, plantedData) == 57
    assert colouredGraphCount(10, plantedData) == 710_249
    assert colouredGraphCount(100, plantedData) == 919_747_298


if __name__ == "__main__":
    start = time.time()
    data = computePlanted(TARGET)
    runTests(data)
    answer = colouredGraphCount(TARGET, data)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
