import time


NORTH, EAST, SOUTH, WEST = range(4)
MOVES = {
    NORTH: (0, 1),
    EAST: (1, 0),
    SOUTH: (0, -1),
    WEST: (-1, 0),
}


def rotate(dx, dy, direction):
    if direction == NORTH:
        return dx, dy
    if direction == EAST:
        return dy, -dx
    if direction == SOUTH:
        return -dx, -dy
    return -dy, dx


def compose(first, second):
    first_steps, first_dx, first_dy, first_turn = first
    second_steps, second_dx, second_dy, second_turn = second
    rotated_dx, rotated_dy = rotate(second_dx, second_dy, first_turn)

    return (
        first_steps + second_steps,
        first_dx + rotated_dx,
        first_dy + rotated_dy,
        (first_turn + second_turn) % 4,
    )


def transforms(limit):
    a_transforms = [(0, 0, 0, 0)]
    b_transforms = [(0, 0, 0, 0)]
    forward = (1, 0, 1, 0)
    right = (0, 0, 0, 1)
    left = (0, 0, 0, 3)

    for level in range(1, limit + 1):
        a = compose(
            compose(compose(compose(a_transforms[level - 1], right), b_transforms[level - 1]), forward),
            right,
        )
        b = compose(
            compose(compose(compose(left, forward), a_transforms[level - 1]), left),
            b_transforms[level - 1],
        )
        a_transforms.append(a)
        b_transforms.append(b)

    return a_transforms, b_transforms


def applyTransform(state, transform):
    x, y, direction = state
    _, dx, dy, turn = transform
    rotated_dx, rotated_dy = rotate(dx, dy, direction)
    return x + rotated_dx, y + rotated_dy, (direction + turn) % 4


def moveForward(state):
    x, y, direction = state
    dx, dy = MOVES[direction]
    return x + dx, y + dy, direction


def walkSymbol(symbol, level, steps, state, a_transforms, b_transforms):
    if steps == 0:
        return state, 0

    transform = a_transforms[level] if symbol == "A" else b_transforms[level]
    if steps >= transform[0]:
        return applyTransform(state, transform), steps - transform[0]

    if symbol == "A":
        components = [("A", level - 1), "R", ("B", level - 1), "F", "R"]
    else:
        components = ["L", "F", ("A", level - 1), "L", ("B", level - 1)]

    return walkComponents(components, steps, state, a_transforms, b_transforms)


def walkComponents(components, steps, state, a_transforms, b_transforms):
    for component in components:
        if steps == 0:
            return state, 0

        if component == "F":
            state = moveForward(state)
            steps -= 1
        elif component == "R":
            x, y, direction = state
            state = x, y, (direction + 1) % 4
        elif component == "L":
            x, y, direction = state
            state = x, y, (direction + 3) % 4
        else:
            state, steps = walkSymbol(
                component[0], component[1], steps, state, a_transforms, b_transforms
            )

    return state, steps


def dragonPosition(level, steps):
    a_transforms, b_transforms = transforms(level)
    state, _ = walkComponents(["F", ("A", level)], steps, (0, 0, NORTH), a_transforms, b_transforms)
    return state[0], state[1]


def runTests():
    assert dragonPosition(0, 1) == (0, 1)
    assert dragonPosition(1, 2) == (1, 1)


if __name__ == "__main__":
    runTests()
    start = time.time()
    x, y = dragonPosition(50, 10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(x) + "," + str(y) + " in " + str(elapsed) + " seconds.")
