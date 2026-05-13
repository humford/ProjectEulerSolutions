from collections import defaultdict
from itertools import permutations
import time


INPUT_FILE = "Files/p424_kakuro200.txt"
LETTERS = "ABCDEFGHIJ"
LETTER_COUNT = len(LETTERS)


def buildDigitTuples():
    digitTuples = {}
    for length in range(1, 7):
        bySum = defaultdict(list)
        for digits in permutations(range(1, 10), length):
            bySum[sum(digits)].append(digits)
        digitTuples[length] = bySum
    return digitTuples


DIGIT_TUPLES = buildDigitTuples()


def splitCells(line):
    cells = []
    current = []
    depth = 0

    for char in line.strip():
        if char == "," and depth == 0:
            cells.append("".join(current))
            current = []
            continue

        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        current.append(char)

    if current:
        cells.append("".join(current))

    return cells


def isWhiteCell(cell):
    return cell == "O" or (len(cell) == 1 and cell in LETTERS)


class KakuroSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.grid = []
        self.runs = []
        self.cellVariables = {}
        self.nextVariable = LETTER_COUNT
        self.parsePuzzle()

        self.variableCount = self.nextVariable
        self.runOptions = []
        self.runVariables = []
        self.variableRuns = [[] for _ in range(self.variableCount)]
        self.buildRunOptions()

    def parsePuzzle(self):
        cells = splitCells(self.puzzle)
        size = int(cells[0])
        gridCells = cells[1:]

        if len(gridCells) != size * size:
            raise ValueError("Puzzle cell count does not match its declared size")

        self.grid = [gridCells[i * size:(i + 1) * size] for i in range(size)]

        for row in range(size):
            for column in range(size):
                cell = self.grid[row][column]
                if cell.startswith("("):
                    for clue in cell[1:-1].split(","):
                        self.addRun(row, column, clue)

    def variableForCell(self, row, column, cell):
        if cell == "O":
            key = (row, column)
            if key not in self.cellVariables:
                self.cellVariables[key] = self.nextVariable
                self.nextVariable += 1
            return self.cellVariables[key]

        return LETTERS.index(cell)

    def addRun(self, row, column, clue):
        direction = clue[0]
        totalCode = clue[1:]
        rowStep, columnStep = (0, 1) if direction == "h" else (1, 0)
        row += rowStep
        column += columnStep
        variables = []

        while (
            0 <= row < len(self.grid)
            and 0 <= column < len(self.grid)
            and isWhiteCell(self.grid[row][column])
        ):
            variables.append(self.variableForCell(row, column, self.grid[row][column]))
            row += rowStep
            column += columnStep

        if not variables:
            raise ValueError("A clue did not point to any white cells")

        self.runs.append((totalCode, tuple(variables)))

    def buildRunOptions(self):
        for totalCode, variables in self.runs:
            options = []
            seen = set()

            for total, tuples in DIGIT_TUPLES[len(variables)].items():
                if len(totalCode) == 1 and total >= 10:
                    continue
                if len(totalCode) == 2 and total < 10:
                    continue

                for digits in tuples:
                    assignments = self.assignmentsForRun(totalCode, variables, total, digits)
                    if assignments is None:
                        continue

                    option = tuple(sorted(assignments.items()))
                    if option not in seen:
                        seen.add(option)
                        options.append(option)

            if not options:
                raise ValueError("A run has no possible digit assignments")

            runIndex = len(self.runOptions)
            self.runOptions.append(options)
            variablesInRun = tuple(sorted({variable for option in options for variable, _ in option}))
            self.runVariables.append(variablesInRun)
            for variable in variablesInRun:
                self.variableRuns[variable].append(runIndex)

    def assignmentsForRun(self, totalCode, variables, total, digits):
        assignments = {}

        def addAssignment(variable, digit):
            previous = assignments.get(variable)
            if previous is not None and previous != digit:
                return False
            assignments[variable] = digit
            return True

        if len(totalCode) == 1:
            if not addAssignment(LETTERS.index(totalCode), total):
                return None
        else:
            if not addAssignment(LETTERS.index(totalCode[0]), total // 10):
                return None
            if not addAssignment(LETTERS.index(totalCode[1]), total % 10):
                return None

        for variable, digit in zip(variables, digits):
            if not addAssignment(variable, digit):
                return None

        assignedLetters = {}
        for variable, digit in assignments.items():
            if variable < LETTER_COUNT:
                if digit in assignedLetters and assignedLetters[digit] != variable:
                    return None
                assignedLetters[digit] = variable

        return assignments

    @staticmethod
    def optionDigit(option, variable):
        for optionVariable, digit in option:
            if optionVariable == variable:
                return digit
        raise KeyError(variable)

    @staticmethod
    def optionCompatible(option, assignments, usedLetterDigits):
        for variable, digit in option:
            current = assignments[variable]
            if current != -1:
                if current != digit:
                    return False
            elif variable < LETTER_COUNT and usedLetterDigits & (1 << digit):
                return False

        return True

    @staticmethod
    def assign(assignments, usedLetterDigits, variable, digit):
        current = assignments[variable]
        if current != -1:
            return usedLetterDigits if current == digit else None

        if variable < LETTER_COUNT and usedLetterDigits & (1 << digit):
            return None

        assignments[variable] = digit
        if variable < LETTER_COUNT:
            usedLetterDigits |= 1 << digit

        return usedLetterDigits

    def propagate(self, assignments, usedLetterDigits):
        while True:
            changed = False
            compatibleOptions = []

            for options in self.runOptions:
                compatible = [
                    option
                    for option in options
                    if self.optionCompatible(option, assignments, usedLetterDigits)
                ]
                if not compatible:
                    return None
                compatibleOptions.append(compatible)

            for runIndex, options in enumerate(compatibleOptions):
                for variable in self.runVariables[runIndex]:
                    if assignments[variable] != -1:
                        continue

                    digit = self.optionDigit(options[0], variable)
                    if all(self.optionDigit(option, variable) == digit for option in options[1:]):
                        updatedDigits = self.assign(assignments, usedLetterDigits, variable, digit)
                        if updatedDigits is None:
                            return None
                        usedLetterDigits = updatedDigits
                        changed = True

            if not changed:
                return assignments, usedLetterDigits, compatibleOptions

    def solve(self):
        solution = None

        def search(assignments, usedLetterDigits):
            nonlocal solution
            if solution is not None:
                return

            propagated = self.propagate(assignments[:], usedLetterDigits)
            if propagated is None:
                return
            assignments, usedLetterDigits, compatibleOptions = propagated

            if all(digit != -1 for digit in assignments):
                solution = assignments
                return

            variable, domain = self.nextSearchVariable(assignments, usedLetterDigits, compatibleOptions)
            if variable is None:
                return

            for digit in sorted(domain):
                nextAssignments = assignments[:]
                nextUsedDigits = self.assign(nextAssignments, usedLetterDigits, variable, digit)
                if nextUsedDigits is not None:
                    search(nextAssignments, nextUsedDigits)

        search([-1] * self.variableCount, 0)
        if solution is None:
            raise ValueError("Puzzle has no solution")

        return solution

    def nextSearchVariable(self, assignments, usedLetterDigits, compatibleOptions):
        bestVariable = None
        bestDomain = None

        for variable, digit in enumerate(assignments):
            if digit != -1:
                continue

            if variable < LETTER_COUNT:
                domain = {digit for digit in range(10) if not usedLetterDigits & (1 << digit)}
            else:
                domain = set(range(1, 10))

            for runIndex in self.variableRuns[variable]:
                domain &= {
                    self.optionDigit(option, variable)
                    for option in compatibleOptions[runIndex]
                }

            if not domain:
                return None, None

            if bestDomain is None or len(domain) < len(bestDomain):
                bestVariable = variable
                bestDomain = domain

        return bestVariable, bestDomain

    @staticmethod
    def puzzleAnswer(solution):
        return int("".join(str(solution[index]) for index in range(LETTER_COUNT)))


def readPuzzles(filename=INPUT_FILE):
    with open(filename) as file:
        return [line.strip() for line in file if line.strip()]


def solvePuzzle(puzzle):
    solver = KakuroSolver(puzzle)
    return solver.puzzleAnswer(solver.solve())


def sumPuzzleAnswers(puzzles):
    return sum(solvePuzzle(puzzle) for puzzle in puzzles)


def allPuzzleAnswerSum():
    return sumPuzzleAnswers(readPuzzles())


def runTests():
    puzzles = readPuzzles()
    assert len(puzzles) == 200
    assert splitCells(puzzles[0])[0] == "6"
    assert solvePuzzle(puzzles[0]) == 8426039571
    assert sumPuzzleAnswers(puzzles[:10]) == 64414157580


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = allPuzzleAnswerSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
