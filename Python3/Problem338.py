import time
from math import isqrt


LIMIT = 10**12
MODULUS = 10**8


def integerCubeRoot(number):
    root = int(round(number ** (1 / 3)))

    while (root + 1) ** 3 <= number:
        root += 1

    while root ** 3 > number:
        root -= 1

    return root


def divisorSummatory(number, modulus=None):
    if number <= 0:
        return 0

    total = 0
    divisor = 1

    while divisor <= number:
        quotient = number // divisor
        nextDivisor = number // quotient
        total += quotient * (nextDivisor - divisor + 1)

        if modulus:
            total %= modulus

        divisor = nextDivisor + 1

    return total % modulus if modulus else total


def tripleDivisorSummatory(number, modulus=None):
    cubeRoot = integerCubeRoot(number)
    total = 0

    for first in range(1, cubeRoot + 1):
        quotient = number // first
        squareRoot = isqrt(quotient)

        subtotal = 0

        for second in range(1, squareRoot + 1):
            term = quotient // second

            if second <= cubeRoot:
                subtotal += term
            else:
                subtotal += 2 * term

        subtotal -= squareRoot * squareRoot
        total += subtotal

        if modulus:
            total %= modulus

    result = 3 * total + cubeRoot**3

    return result % modulus if modulus else result


def floorProductSum(limit, modulus=None):
    total = 0
    index = 2

    while index <= limit:
        first = limit // index
        second = limit // (index - 1)
        nextFirst = limit // first + 1
        previous = index - 1
        nextSecond = limit // second + 2
        nextIndex = min(nextFirst, nextSecond, limit + 1)

        total += (nextIndex - index) * first * second

        if modulus:
            total %= modulus

        index = nextIndex

    return total % modulus if modulus else total


def divisorSummatoryFloorSum(limit, modulus=None):
    # sum_{i=2..n} D(floor(n/i)) is the triple-divisor summatory D_3(n)
    # with the i=1 divisor-summatory term removed.
    total = tripleDivisorSummatory(limit, modulus) - divisorSummatory(limit, modulus)

    return total % modulus if modulus else total


def gridPaperSum(limit):
    return floorProductSum(limit) - divisorSummatoryFloorSum(limit)


def gridPaperSumMod(limit=LIMIT):
    return (
        floorProductSum(limit, MODULUS)
        - divisorSummatoryFloorSum(limit, MODULUS)
    ) % MODULUS


def referenceRectangleCount(width, height):
    if height > width:
        width, height = height, width

    rectangles = set()

    for cuts in range(1, width + 1):
        if width % cuts != 0:
            continue

        if height % (cuts + 1) == 0:
            newWidth = width * (cuts + 1) // cuts
            newHeight = height * cuts // (cuts + 1)
            rectangles.add(tuple(sorted((newWidth, newHeight), reverse=True)))

        if cuts >= 2 and height % (cuts - 1) == 0:
            newWidth = width * (cuts - 1) // cuts
            newHeight = height * cuts // (cuts - 1)
            rectangles.add(tuple(sorted((newWidth, newHeight), reverse=True)))

    rectangles.discard((width, height))
    return len(rectangles)


def runTests():
    assert referenceRectangleCount(2, 1) == 0
    assert referenceRectangleCount(2, 2) == 1
    assert referenceRectangleCount(9, 4) == 3
    assert referenceRectangleCount(9, 8) == 2
    assert gridPaperSumMod(10) == 55
    assert gridPaperSumMod(10**3) == 971745
    assert gridPaperSum(10**5) == 9992617687


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gridPaperSumMod()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
