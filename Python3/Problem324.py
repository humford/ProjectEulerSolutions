import time


MODULUS = 100000007
WIDTH = 3
CELLS = WIDTH * WIDTH
FULL_LAYER = (1 << CELLS) - 1
TARGET = 10**10000


def layerTransitions(mask):
    transitions = {}

    def fill(currentMask, nextMask):
        if currentMask == FULL_LAYER:
            transitions[nextMask] = transitions.get(nextMask, 0) + 1
            return

        cell = 0
        while (currentMask >> cell) & 1:
            cell += 1

        fill(currentMask | (1 << cell), nextMask | (1 << cell))

        row, column = divmod(cell, WIDTH)

        if column + 1 < WIDTH:
            neighbor = cell + 1
            if not (currentMask >> neighbor) & 1:
                fill(currentMask | (1 << cell) | (1 << neighbor), nextMask)

        if row + 1 < WIDTH:
            neighbor = cell + WIDTH
            if not (currentMask >> neighbor) & 1:
                fill(currentMask | (1 << cell) | (1 << neighbor), nextMask)

    fill(mask, 0)
    return transitions


TRANSITIONS = [layerTransitions(mask) for mask in range(1 << CELLS)]


def generateTowerCounts(count):
    dp = [0] * (1 << CELLS)
    dp[0] = 1
    sequence = [1]

    for _ in range(count):
        nextDp = [0] * (1 << CELLS)

        for mask, value in enumerate(dp):
            if value == 0:
                continue

            for nextMask, ways in TRANSITIONS[mask].items():
                nextDp[nextMask] = (nextDp[nextMask] + value * ways) % MODULUS

        dp = nextDp
        sequence.append(dp[0])

    return sequence


def berlekampMassey(sequence):
    current = [1]
    previous = [1]
    length = 0
    shift = 1
    previousDiscrepancy = 1

    for index, value in enumerate(sequence):
        discrepancy = value

        for coefficient in range(1, length + 1):
            discrepancy = (
                discrepancy + current[coefficient] * sequence[index - coefficient]
            ) % MODULUS

        if discrepancy == 0:
            shift += 1
            continue

        oldCurrent = current[:]
        scale = discrepancy * pow(previousDiscrepancy, MODULUS - 2, MODULUS) % MODULUS

        if len(current) < len(previous) + shift:
            current.extend([0] * (len(previous) + shift - len(current)))

        for coefficient in range(len(previous)):
            current[coefficient + shift] = (
                current[coefficient + shift] - scale * previous[coefficient]
            ) % MODULUS

        if 2 * length <= index:
            length = index + 1 - length
            previous = oldCurrent
            previousDiscrepancy = discrepancy
            shift = 1
        else:
            shift += 1

    return [(-current[index]) % MODULUS for index in range(1, length + 1)]


def linearRecurrenceValue(coefficients, initialValues, index):
    length = len(coefficients)

    def combine(left, right):
        result = [0] * (2 * length)

        for i in range(length):
            if left[i] == 0:
                continue

            for j in range(length):
                result[i + j] = (result[i + j] + left[i] * right[j]) % MODULUS

        for i in range(2 * length - 2, length - 1, -1):
            if result[i] == 0:
                continue

            for j in range(1, length + 1):
                result[i - j] = (
                    result[i - j] + result[i] * coefficients[j - 1]
                ) % MODULUS

        return result[:length]

    polynomial = [1] + [0] * (length - 1)
    power = [0] * length

    if length == 1:
        power[0] = coefficients[0]
    else:
        power[1] = 1

    while index > 0:
        if index & 1:
            polynomial = combine(polynomial, power)

        power = combine(power, power)
        index //= 2

    return sum(
        polynomial[index] * initialValues[index] for index in range(length)
    ) % MODULUS


def towerCount(index=TARGET):
    sequence = generateTowerCounts(100)
    coefficients = berlekampMassey(sequence)
    return linearRecurrenceValue(coefficients, sequence[: len(coefficients)], index)


def runTests():
    sequence = generateTowerCounts(100)
    coefficients = berlekampMassey(sequence)

    assert sequence[2] == 229
    assert sequence[4] == 117805
    assert sequence[10] == 96149360
    assert (
        linearRecurrenceValue(coefficients, sequence[: len(coefficients)], 10**3)
        == 24806056
    )
    assert (
        linearRecurrenceValue(coefficients, sequence[: len(coefficients)], 10**6)
        == 30808124
    )


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = towerCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
