import time


def nextChef(chef, mask):
    higher = mask & ~((1 << (chef + 1)) - 1)
    if higher:
        return (higher & -higher).bit_length() - 1
    return (mask & -mask).bit_length() - 1


def solveGame(skills):
    chefCount = len(skills)
    fullMask = (1 << chefCount) - 1
    winProbabilities = [
        [[0.0 for _ in range(chefCount)] for _ in range(chefCount)]
        for _ in range(1 << chefCount)
    ]
    expectedDishes = [
        [0.0 for _ in range(chefCount)]
        for _ in range(1 << chefCount)
    ]

    for chef in range(chefCount):
        mask = 1 << chef
        winProbabilities[mask][chef][chef] = 1.0

    masksBySize = [[] for _ in range(chefCount + 1)]
    for mask in range(1, 1 << chefCount):
        masksBySize[mask.bit_count()].append(mask)

    for size in range(2, chefCount + 1):
        for mask in masksBySize[size]:
            chefs = [
                chef for chef in range(chefCount)
                if (mask >> chef) & 1
            ]
            positions = {chef: index for index, chef in enumerate(chefs)}
            activeCount = len(chefs)
            missProbability = [0.0] * activeCount
            hitWinVectors = [[0.0] * chefCount for _ in range(activeCount)]
            hitExpectations = [0.0] * activeCount

            for index, chef in enumerate(chefs):
                skill = skills[chef]
                missProbability[index] = 1.0 - skill
                bestWinChance = -1.0
                tiedEliminations = []

                for eliminated in chefs:
                    if eliminated == chef:
                        continue
                    nextMask = mask & ~(1 << eliminated)
                    nextTurn = nextChef(chef, nextMask)
                    winChance = winProbabilities[nextMask][nextTurn][chef]

                    if winChance > bestWinChance + 1e-15:
                        bestWinChance = winChance
                        tiedEliminations = [eliminated]
                    elif abs(winChance - bestWinChance) <= 1e-15:
                        tiedEliminations.append(eliminated)

                if len(tiedEliminations) == 1:
                    eliminated = tiedEliminations[0]
                else:
                    chefPosition = positions[chef]

                    def turnDistance(other):
                        distance = positions[other] - chefPosition
                        if distance <= 0:
                            distance += activeCount
                        return distance

                    eliminated = min(tiedEliminations, key=turnDistance)

                nextMask = mask & ~(1 << eliminated)
                nextTurn = nextChef(chef, nextMask)
                hitWinVectors[index] = [
                    skill * value
                    for value in winProbabilities[nextMask][nextTurn]
                ]
                hitExpectations[index] = (
                    skill * expectedDishes[nextMask][nextTurn]
                )

            coefficients = [0.0] * activeCount
            constants = [[0.0] * chefCount for _ in range(activeCount)]
            nextCoefficient = 1.0
            nextConstant = [0.0] * chefCount
            for index in range(activeCount - 1, -1, -1):
                coefficients[index] = missProbability[index] * nextCoefficient
                constants[index] = [
                    missProbability[index] * nextConstant[chef]
                    + hitWinVectors[index][chef]
                    for chef in range(chefCount)
                ]
                nextCoefficient = coefficients[index]
                nextConstant = constants[index]

            firstWinVector = [
                value / (1.0 - coefficients[0])
                for value in constants[0]
            ]
            for index, chef in enumerate(chefs):
                winProbabilities[mask][chef] = [
                    coefficients[index] * firstWinVector[winner]
                    + constants[index][winner]
                    for winner in range(chefCount)
                ]

            expectationCoefficients = [0.0] * activeCount
            expectationConstants = [0.0] * activeCount
            nextCoefficient = 1.0
            nextConstant = 0.0
            for index in range(activeCount - 1, -1, -1):
                expectationCoefficients[index] = (
                    missProbability[index] * nextCoefficient
                )
                expectationConstants[index] = (
                    1.0
                    + missProbability[index] * nextConstant
                    + hitExpectations[index]
                )
                nextCoefficient = expectationCoefficients[index]
                nextConstant = expectationConstants[index]

            firstExpectation = (
                expectationConstants[0] / (1.0 - expectationCoefficients[0])
            )
            for index, chef in enumerate(chefs):
                expectedDishes[mask][chef] = (
                    expectationCoefficients[index] * firstExpectation
                    + expectationConstants[index]
                )

    return winProbabilities, expectedDishes, fullMask


def fibonacciSkills(chefCount):
    fibonacci = [0] * (chefCount + 2)
    fibonacci[1] = fibonacci[2] = 1
    for index in range(3, chefCount + 2):
        fibonacci[index] = fibonacci[index - 1] + fibonacci[index - 2]

    denominator = fibonacci[chefCount + 1]
    return [
        fibonacci[index + 1] / denominator
        for index in range(chefCount)
    ]


def chefWinProbabilities(n):
    winProbabilities, _, fullMask = solveGame(fibonacciSkills(n))
    return [
        format(winProbabilities[fullMask][0][chef], ".8f")
        for chef in range(n)
    ]


def expectedDishesForChefs(n):
    _, expectedDishes, fullMask = solveGame(fibonacciSkills(n))
    return format(expectedDishes[fullMask][0], ".8f")


def runTests():
    winProbabilities, _, fullMask = solveGame([0.25, 0.5, 1.0])
    assert abs(winProbabilities[fullMask][0][0] - 0.29375) < 1e-12

    assert chefWinProbabilities(7) == [
        "0.08965042",
        "0.20775702",
        "0.15291406",
        "0.14554098",
        "0.15905291",
        "0.10261412",
        "0.14247050",
    ]
    assert expectedDishesForChefs(7) == "42.28176050"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedDishesForChefs(14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
