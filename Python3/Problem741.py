import time


MODULUS = 1_000_000_007
INVERSE_TWO = (MODULUS + 1) // 2
INVERSE_EIGHT = pow(8, MODULUS - 2, MODULUS)


def gridCountDiagonalFixAndFactorial(size):
    factorial = 1
    hPreviousPrevious = 1
    hPrevious = 0

    if size >= 4:
        diagonal0, diagonal1, diagonal2, diagonal3 = 1, 0, 1, 4

    for number in range(1, size + 1):
        factorial = factorial * number % MODULUS

        if number >= 2:
            k = number - 1
            hCurrent = (k * hPrevious + (k * INVERSE_TWO % MODULUS) * hPreviousPrevious) % MODULUS
            hPreviousPrevious, hPrevious = hPrevious, hCurrent

        if size >= 4 and number >= 4:
            k = number - 1
            nextDiagonal = (
                2 * k * diagonal3
                - k * (k - 2) * diagonal2
                - (k * (k - 1) % MODULUS) * (k - 2) * diagonal0 * INVERSE_TWO
            ) % MODULUS
            diagonal0, diagonal1, diagonal2, diagonal3 = diagonal1, diagonal2, diagonal3, nextDiagonal

    gridCount = factorial * hPrevious % MODULUS

    if size == 0:
        diagonalFix = 1
    elif size == 1:
        diagonalFix = 0
    elif size == 2:
        diagonalFix = 1
    elif size == 3:
        diagonalFix = 4
    else:
        diagonalFix = diagonal3

    return gridCount, diagonalFix, factorial


def axisReflectionFix(size, factorial):
    if size & 1:
        return 0
    return factorial * pow(INVERSE_TWO, size // 2, MODULUS) % MODULUS


def rotation90Fix(size):
    if size & 1:
        return 0

    halfSize = size // 2
    if halfSize == 0:
        return 1
    if halfSize == 1:
        return 1
    if halfSize == 2:
        return 2

    b0, b1, b2 = 1, 1, 2
    for number in range(2, halfSize):
        nextValue = ((2 * number + 1) * b2 - number * b1 + 2 * number * (number - 1) * b0) % MODULUS
        b0, b1, b2 = b1, b2, nextValue
    return b2


def rotation180Fix(size):
    if size == 0:
        return 1

    if size % 2 == 0:
        halfSize = size // 2
        if halfSize == 0:
            return 1
        if halfSize == 1:
            return 1

        jPrevious, jCurrent = 1, 1
        factorial = 1
        for number in range(1, halfSize):
            factorial = factorial * number % MODULUS
            nextJ = ((4 * number + 1) * jCurrent + 4 * number * jPrevious) % MODULUS
            jPrevious, jCurrent = jCurrent, nextJ

        halfFactorial = factorial * halfSize % MODULUS
        return halfFactorial * jCurrent % MODULUS

    halfSize = (size - 1) // 2
    if halfSize == 0:
        return 0

    factorial = 1
    tValue = 0
    jPrevious, jCurrent = 1, 1
    for number in range(1, halfSize + 1):
        factorial = factorial * number % MODULUS
        tValue = (4 * number * tValue + 2 * number * jPrevious) % MODULUS
        if number < halfSize:
            nextJ = ((4 * number + 1) * jCurrent + 4 * number * jPrevious) % MODULUS
            jPrevious, jCurrent = jCurrent, nextJ

    return factorial * tValue % MODULUS


def gridColouringCount(size):
    return gridCountDiagonalFixAndFactorial(size)[0]


def uniqueGridColouringCount(size):
    gridCount, diagonalFix, factorial = gridCountDiagonalFixAndFactorial(size)
    axisFix = axisReflectionFix(size, factorial)
    rotation180 = rotation180Fix(size)
    rotation90 = rotation90Fix(size)

    burnsideTotal = (gridCount + rotation180 + 2 * rotation90 + 2 * axisFix + 2 * diagonalFix) % MODULUS
    return burnsideTotal * INVERSE_EIGHT % MODULUS


def targetUniqueGridColouringSum():
    return (uniqueGridColouringCount(7**7) + uniqueGridColouringCount(8**8)) % MODULUS


def runTests():
    assert gridColouringCount(4) == 90
    assert gridColouringCount(7) == 3_110_940
    assert gridColouringCount(8) == 187_530_840
    assert uniqueGridColouringCount(4) == 20
    assert uniqueGridColouringCount(7) == 390_816
    assert uniqueGridColouringCount(8) == 23_462_347
    assert uniqueGridColouringCount(7) + uniqueGridColouringCount(8) == 23_853_163


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = targetUniqueGridColouringSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
