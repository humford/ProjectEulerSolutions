import time


TARGET = 500


def buildPentadiagonal(size):
    lowerTwo = [0.0] * size
    lowerOne = [0.0] * size
    diagonal = [6.0] * size
    upperOne = [0.0] * size
    upperTwo = [0.0] * size

    for i in range(size):
        if i - 1 >= 0:
            lowerOne[i] = -2.0
        if i + 1 < size:
            upperOne[i] = -2.0
        if i - 2 >= 0:
            lowerTwo[i] = -1.0
        if i + 2 < size:
            upperTwo[i] = -1.0

    return lowerTwo, lowerOne, diagonal, upperOne, upperTwo


def factorPentadiagonal(lowerTwo, lowerOne, diagonal, upperOne, upperTwo):
    size = len(diagonal)
    lowerOne = lowerOne[:]
    diagonal = diagonal[:]
    upperOne = upperOne[:]
    upperTwo = upperTwo[:]
    alpha = [0.0] * size
    beta = [0.0] * size

    for i in range(size):
        pivot = diagonal[i]
        if i + 1 < size:
            alpha[i + 1] = lowerOne[i + 1] / pivot
            diagonal[i + 1] -= alpha[i + 1] * upperOne[i]
            if i + 2 < size:
                upperOne[i + 1] -= alpha[i + 1] * upperTwo[i]
        if i + 2 < size:
            beta[i + 2] = lowerTwo[i + 2] / pivot
            lowerOne[i + 2] -= beta[i + 2] * upperOne[i]
            diagonal[i + 2] -= beta[i + 2] * upperTwo[i]

    return diagonal, upperOne, upperTwo, alpha, beta


def solveFactoredPentadiagonal(diagonal, upperOne, upperTwo, alpha, beta, rhs):
    size = len(diagonal)
    rhs = rhs[:]

    for i in range(size):
        if i + 1 < size:
            rhs[i + 1] -= alpha[i + 1] * rhs[i]
        if i + 2 < size:
            rhs[i + 2] -= beta[i + 2] * rhs[i]

    solution = [0.0] * size
    solution[-1] = rhs[-1] / diagonal[-1]
    if size >= 2:
        solution[-2] = (
            rhs[-2] - upperOne[-2] * solution[-1]
        ) / diagonal[-2]

    for i in range(size - 3, -1, -1):
        solution[i] = (
            rhs[i]
            - upperOne[i] * solution[i + 1]
            - upperTwo[i] * solution[i + 2]
        ) / diagonal[i]

    return solution


class CyclicPentadiagonalSolver:
    def __init__(self, size):
        self.size = size
        bands = buildPentadiagonal(size)
        self.diagonal, self.upperOne, self.upperTwo, self.alpha, self.beta = (
            factorPentadiagonal(*bands)
        )

        firstCorner = [0.0] * size
        lastCorner = [0.0] * size
        firstCorner[0] = -1.0
        lastCorner[-1] = -1.0
        self.firstCorrection = solveFactoredPentadiagonal(
            self.diagonal,
            self.upperOne,
            self.upperTwo,
            self.alpha,
            self.beta,
            firstCorner,
        )
        self.lastCorrection = solveFactoredPentadiagonal(
            self.diagonal,
            self.upperOne,
            self.upperTwo,
            self.alpha,
            self.beta,
            lastCorner,
        )

        m00 = 1.0 + self.firstCorrection[-1]
        m01 = self.lastCorrection[-1]
        m10 = self.firstCorrection[0]
        m11 = 1.0 + self.lastCorrection[0]
        determinant = m00 * m11 - m01 * m10
        self.inverse00 = m11 / determinant
        self.inverse01 = -m01 / determinant
        self.inverse10 = -m10 / determinant
        self.inverse11 = m00 / determinant

    def solve(self, rhs):
        solution = solveFactoredPentadiagonal(
            self.diagonal,
            self.upperOne,
            self.upperTwo,
            self.alpha,
            self.beta,
            rhs,
        )

        rightValue = solution[-1]
        leftValue = solution[0]
        firstWeight = self.inverse00 * rightValue + self.inverse01 * leftValue
        lastWeight = self.inverse10 * rightValue + self.inverse11 * leftValue

        return [
            solution[i]
            - self.firstCorrection[i] * firstWeight
            - self.lastCorrection[i] * lastWeight
            for i in range(self.size)
        ]


def expectedRoundPayment(players):
    if players == 2:
        firstMoment = 9.0 / 4.0
        weightedNextFirstMoment = (5.0 / 9.0) * firstMoment
        secondMoment = (9.0 + 18.0 * weightedNextFirstMoment) / 4.0
        return secondMoment / players

    stateCount = players - 1
    solver = CyclicPentadiagonalSolver(stateCount)
    firstMoments = solver.solve([9.0] * stateCount)
    firstMomentsByState = [0.0] + firstMoments

    secondMomentRhs = [0.0] * stateCount
    for state in range(1, players):
        weightedNext = (
            (1.0 / 3.0) * firstMomentsByState[state]
            + (2.0 / 9.0) * (
                firstMomentsByState[(state - 1) % players]
                + firstMomentsByState[(state + 1) % players]
            )
            + (1.0 / 9.0) * (
                firstMomentsByState[(state - 2) % players]
                + firstMomentsByState[(state + 2) % players]
            )
        )
        secondMomentRhs[state - 1] = 9.0 + 18.0 * weightedNext

    secondMoments = solver.solve(secondMomentRhs)
    return sum(secondMoments) / players


def expectedChasePot(players):
    return sum(expectedRoundPayment(roundPlayers)
               for roundPlayers in range(2, players + 1))


def scientificNineDigits(value):
    mantissa, exponent = f"{value:.8e}".split("e")
    return mantissa + "e" + str(int(exponent))


def runTests():
    assert round(expectedChasePot(5), 3) == 96.544
    assert scientificNineDigits(expectedChasePot(50)) == "2.82491788e6"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = scientificNineDigits(expectedChasePot(TARGET))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
