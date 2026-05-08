import time
from pathlib import Path


ALL_DIGITS = sum(1 << digit for digit in range(1, 10))


def readPuzzles():
    path = Path(__file__).resolve().parents[1] / "Files" / "p096_sudoku.txt"
    lines = path.read_text().strip().splitlines()
    puzzles = []

    for index in range(0, len(lines), 10):
        puzzle = []
        for row in lines[index + 1 : index + 10]:
            puzzle.extend(int(char) for char in row)
        puzzles.append(puzzle)

    return puzzles


def boxIndex(position):
    row = position // 9
    col = position % 9
    return (row // 3) * 3 + col // 3


def solve(grid):
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empty_positions = []

    for position, digit in enumerate(grid):
        if digit == 0:
            empty_positions.append(position)
            continue

        bit = 1 << digit
        row = position // 9
        col = position % 9
        box = boxIndex(position)
        rows[row] |= bit
        cols[col] |= bit
        boxes[box] |= bit

    def search():
        best_position = None
        best_candidates = None

        for position in empty_positions:
            if grid[position] != 0:
                continue

            row = position // 9
            col = position % 9
            box = boxIndex(position)
            candidates = ALL_DIGITS & ~(rows[row] | cols[col] | boxes[box])
            if candidates == 0:
                return False
            if best_candidates is None or candidates.bit_count() < best_candidates.bit_count():
                best_position = position
                best_candidates = candidates

        if best_position is None:
            return True

        row = best_position // 9
        col = best_position % 9
        box = boxIndex(best_position)
        candidates = best_candidates

        while candidates:
            bit = candidates & -candidates
            digit = bit.bit_length() - 1
            candidates -= bit

            grid[best_position] = digit
            rows[row] |= bit
            cols[col] |= bit
            boxes[box] |= bit

            if search():
                return True

            rows[row] ^= bit
            cols[col] ^= bit
            boxes[box] ^= bit
            grid[best_position] = 0

        return False

    if not search():
        raise ValueError("Puzzle has no solution")
    return grid


def topLeftNumber(grid):
    return 100 * grid[0] + 10 * grid[1] + grid[2]


def sumTopLeftNumbers(puzzles):
    return sum(topLeftNumber(solve(puzzle[:])) for puzzle in puzzles)


def runTests():
    solved = [int(char) for char in "534678912672195348198342567859761423426853791713924856961537284287419635345286179"]
    puzzle = solved[:]
    puzzle[0] = 0
    assert solve(puzzle)[0] == 5
    assert topLeftNumber(solved) == 534


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumTopLeftNumbers(readPuzzles())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
