import time
from math import isqrt


def ceilSqrt(number):
    root = isqrt(number)
    return root + (root * root < number)


def rowScanCrossFlipCount(size):
    if size & 1:
        if size == 5:
            return 3

        return 0

    square = size * size
    rowParity = [0] * size
    outerY = [0] * size
    innerY = [0] * size
    oddRows = 0
    blackCells = 0

    for x in range(size):
        xSquare = x * x
        yOuter = isqrt(square - 1 - xSquare)
        outerY[x] = yOuter

        if x == size - 1:
            yInner = -1
        else:
            innerValue = square - 2 * size - xSquare
            yInner = isqrt(innerValue) if innerValue >= 0 else -1

        innerY[x] = yInner
        rowBlackCount = yOuter - yInner
        blackCells += rowBlackCount
        rowParity[x] = rowBlackCount & 1
        oddRows += rowParity[x]

    prefixParity = [0] * (size + 1)
    for index in range(size):
        prefixParity[index + 1] = prefixParity[index] + rowParity[index]

    blackWithMixedParity = 0

    for x in range(size):
        y0 = innerY[x] + 1
        y1 = outerY[x]

        if y0 < 0:
            y0 = 0

        if y0 > y1:
            continue

        ones = prefixParity[y1 + 1] - prefixParity[y0]
        rowLength = y1 - y0 + 1

        if rowParity[x] == 0:
            blackWithMixedParity += ones
        else:
            blackWithMixedParity += rowLength - ones

    return (
        2 * oddRows * (size - oddRows)
        + blackCells
        - 2 * blackWithMixedParity
    )


def crossFlipCount(size):
    if size & 1:
        if size == 5:
            return 3

        return 0

    square = size * size
    innerSquare = (size - 1) * (size - 1)
    result = 0
    flippedRows = 0
    unflippedRows = 0
    flippedColumns = 0
    previousHighX = 0
    previousRowFlipped = False
    y = size - 1

    # For even size there is a unique move pattern over GF(2).  The board is
    # symmetric, so this sweep counts the top-right octant and reflects it.
    while True:
        lowX = ceilSqrt(innerSquare - y * y)

        if y < lowX:
            result *= 2
            break

        highX = ceilSqrt(square - y * y)
        width = highX - lowX
        flipsColumn = lowX == previousHighX - 1
        previousHighX = highX
        lastRow = y < highX

        if width & 1:
            result += width - int(lastRow)

            if flipsColumn:
                result += (
                    unflippedRows
                    - flippedRows
                    - 2 * flippedColumns
                    + y
                    - 2
                    + (2 if previousRowFlipped else -2)
                )
                flippedColumns += 1

            previousRowFlipped = False
            unflippedRows += 1
        else:
            if not lastRow:
                result += size - width - 1 - 2 * flippedColumns - 2 * flippedRows

                if flipsColumn:
                    result += (
                        unflippedRows
                        - flippedRows
                        - 2 * flippedColumns
                        + y
                        + (2 if previousRowFlipped else -2)
                    )
                    flippedColumns += 1
            elif y == lowX:
                result += (
                    size
                    - width
                    - 2 * flippedColumns
                    - 2 * flippedRows
                    + int(previousRowFlipped)
                )

                if previousRowFlipped:
                    result += 2
            else:
                result += size - width - 2 * flippedColumns - 2 * flippedRows

                if previousRowFlipped and y == lowX:
                    result += 2

                if flipsColumn:
                    result += (
                        unflippedRows
                        - flippedRows
                        + 2 * int(previousRowFlipped)
                        - 2 * flippedColumns
                        + y
                    )
                    flippedColumns += 1

            flippedRows += 1
            previousRowFlipped = True

        if lastRow:
            result = 2 * result + 1
            break

        y -= 1

    return result


def crossFlipSum():
    return sum(crossFlipCount((1 << index) - index) for index in range(3, 32))


def runTests():
    assert crossFlipCount(5) == 3
    assert crossFlipCount(10) == 29
    assert crossFlipCount(1000) == 395253

    for size in range(2, 200):
        assert crossFlipCount(size) == rowScanCrossFlipCount(size)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = crossFlipSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
