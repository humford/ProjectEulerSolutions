import time


SIZE = 5
FULL_ROW = (1 << SIZE) - 1
TOP_ROW = 0
BOTTOM_ROW = SIZE - 1
START_POSITION = 2 * SIZE + 2


NEIGHBORS = []
for y in range(SIZE):
    for x in range(SIZE):
        neighbors = []
        if x > 0:
            neighbors.append(y * SIZE + x - 1)
        if x < SIZE - 1:
            neighbors.append(y * SIZE + x + 1)
        if y > 0:
            neighbors.append((y - 1) * SIZE + x)
        if y < SIZE - 1:
            neighbors.append((y + 1) * SIZE + x)
        NEIGHBORS.append(tuple(neighbors))


MASKS_BY_COUNT = [[] for _ in range(SIZE + 1)]
for mask in range(1 << SIZE):
    MASKS_BY_COUNT[mask.bit_count()].append(mask)


def solvePositionExpectations(targets, boundary_values):
    target_set = set(targets)
    state_count = SIZE * SIZE
    matrix = [[0.0] * (state_count + 1) for _ in range(state_count)]

    for position in range(state_count):
        if position in target_set:
            matrix[position][position] = 1.0
            matrix[position][state_count] = boundary_values[position]
            continue

        matrix[position][position] = 1.0
        probability = 1.0 / len(NEIGHBORS[position])
        for neighbor in NEIGHBORS[position]:
            matrix[position][neighbor] -= probability
        matrix[position][state_count] = 1.0

    for column in range(state_count):
        pivot = max(range(column, state_count), key=lambda row: abs(matrix[row][column]))
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]

        inverse = 1.0 / matrix[column][column]
        for index in range(column, state_count + 1):
            matrix[column][index] *= inverse

        for row in range(state_count):
            if row == column:
                continue

            factor = matrix[row][column]
            if factor == 0:
                continue

            for index in range(column, state_count + 1):
                matrix[row][index] -= factor * matrix[column][index]

    return [matrix[position][state_count] for position in range(state_count)]


def antSeedExpectedSteps():
    not_carrying = {(0, FULL_ROW): [0.0] * (SIZE * SIZE)}
    carrying = {}

    for dropped_count in range(SIZE - 1, -1, -1):
        for top_mask in MASKS_BY_COUNT[dropped_count]:
            top_targets = [
                TOP_ROW * SIZE + x
                for x in range(SIZE)
                if top_mask & (1 << x) == 0
            ]

            for bottom_mask in MASKS_BY_COUNT[SIZE - 1 - dropped_count]:
                boundary_values = [0.0] * (SIZE * SIZE)

                for x in range(SIZE):
                    if top_mask & (1 << x) == 0:
                        position = TOP_ROW * SIZE + x
                        next_top_mask = top_mask | (1 << x)
                        boundary_values[position] = not_carrying[
                            (bottom_mask, next_top_mask)
                        ][position]

                carrying[(bottom_mask, top_mask)] = solvePositionExpectations(
                    top_targets, boundary_values
                )

        for top_mask in MASKS_BY_COUNT[dropped_count]:
            for bottom_mask in MASKS_BY_COUNT[SIZE - dropped_count]:
                bottom_targets = [
                    BOTTOM_ROW * SIZE + x
                    for x in range(SIZE)
                    if bottom_mask & (1 << x)
                ]
                boundary_values = [0.0] * (SIZE * SIZE)

                for x in range(SIZE):
                    if bottom_mask & (1 << x):
                        position = BOTTOM_ROW * SIZE + x
                        next_bottom_mask = bottom_mask ^ (1 << x)
                        boundary_values[position] = carrying[
                            (next_bottom_mask, top_mask)
                        ][position]

                not_carrying[(bottom_mask, top_mask)] = solvePositionExpectations(
                    bottom_targets, boundary_values
                )

    return not_carrying[(FULL_ROW, 0)][START_POSITION]


def runTests():
    zero_boundaries = [0.0] * (SIZE * SIZE)
    assert solvePositionExpectations([START_POSITION], zero_boundaries)[
        START_POSITION
    ] == 0.0


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(antSeedExpectedSteps(), ".6f")
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
