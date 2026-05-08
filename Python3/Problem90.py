import itertools
import time


SQUARES = [(0, 1), (0, 4), (0, 9), (1, 6), (2, 5), (3, 6), (4, 9), (6, 4), (8, 1)]


def hasDigit(cube, digit):
    if digit in (6, 9):
        return 6 in cube or 9 in cube
    return digit in cube


def canDisplay(cube_one, cube_two, square):
    first, second = square
    return (
        hasDigit(cube_one, first)
        and hasDigit(cube_two, second)
        or hasDigit(cube_one, second)
        and hasDigit(cube_two, first)
    )


def canDisplayAllSquares(cube_one, cube_two):
    return all(canDisplay(cube_one, cube_two, square) for square in SQUARES)


def cubePairCount():
    cubes = [set(cube) for cube in itertools.combinations(range(10), 6)]
    count = 0

    for first_index, cube_one in enumerate(cubes):
        for cube_two in cubes[first_index:]:
            if canDisplayAllSquares(cube_one, cube_two):
                count += 1

    return count


def runTests():
    assert hasDigit({0, 1, 2, 3, 4, 6}, 9)
    assert canDisplay({0, 5, 6, 7, 8, 9}, {1, 2, 3, 4, 8, 9}, (0, 1))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cubePairCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
