import time


def _attackMasks(n, reach):
    attacks = [[0] * n for _ in range(reach + 1)]
    for distance in range(1, reach + 1):
        for column in range(n):
            mask = 1 << column
            if column >= distance:
                mask |= 1 << (column - distance)
            if column + distance < n:
                mask |= 1 << (column + distance)
            attacks[distance][column] = mask
    return attacks


def _reflectedFirstRowStates(n):
    states = {column: 2 for column in range(n // 2)}
    if n % 2 == 1:
        states[n // 2] = 1
    return states


def _classicalQueenCount(n):
    fullMask = (1 << n) - 1

    def search(row, columns, leftDiagonals, rightDiagonals):
        if row == n:
            return 1

        available = fullMask & ~(columns | leftDiagonals | rightDiagonals)
        total = 0
        while available:
            bit = available & -available
            available ^= bit
            total += search(
                row + 1,
                columns | bit,
                ((leftDiagonals | bit) << 1) & fullMask,
                (rightDiagonals | bit) >> 1,
            )
        return total

    total = 0
    for column, multiplier in _reflectedFirstRowStates(n).items():
        bit = 1 << column
        total += multiplier * search(
            1,
            bit,
            (bit << 1) & fullMask,
            bit >> 1,
        )
    return total


def _transferQueenCount(n, reach):
    fullMask = (1 << n) - 1
    columnBits = max(1, (n - 1).bit_length())
    columnMask = (1 << columnBits) - 1
    trimMask = (1 << (columnBits * reach)) - 1
    attacks = _attackMasks(n, reach)
    cacheTransitions = reach <= 9
    transitionCache = {}

    def nextStates(state, inspectedRows):
        if cacheTransitions and inspectedRows == reach and state in transitionCache:
            return transitionCache[state]

        forbidden = 0
        savedState = state
        for distance in range(1, inspectedRows + 1):
            forbidden |= attacks[distance][state & columnMask]
            state >>= columnBits

        available = fullMask & ~forbidden
        states = []
        while available:
            bit = available & -available
            available ^= bit
            column = bit.bit_length() - 1
            states.append(((savedState << columnBits) | column) & trimMask)

        if cacheTransitions and inspectedRows == reach:
            transitionCache[savedState] = tuple(states)
        return states

    frontier = _reflectedFirstRowStates(n)
    for row in range(1, n):
        inspectedRows = min(row, reach)
        nextFrontier = {}
        for state, count in frontier.items():
            for nextState in nextStates(state, inspectedRows):
                nextFrontier[nextState] = nextFrontier.get(nextState, 0) + count
        frontier = nextFrontier

    return sum(frontier.values())


def _lateReleaseQueenCount(n, reach):
    fullMask = (1 << n) - 1
    columns = []

    def search(row, usedColumns, leftDiagonals, rightDiagonals):
        if row == n:
            return 1

        if row <= reach:
            available = fullMask & ~(usedColumns | leftDiagonals | rightDiagonals)
        else:
            forbidden = 0
            for priorRow in range(row - reach, row):
                priorColumn = columns[priorRow]
                rowDelta = row - priorRow
                forbidden |= 1 << priorColumn
                if priorColumn >= rowDelta:
                    forbidden |= 1 << (priorColumn - rowDelta)
                if priorColumn + rowDelta < n:
                    forbidden |= 1 << (priorColumn + rowDelta)
            available = fullMask & ~forbidden

        total = 0
        while available:
            bit = available & -available
            available ^= bit
            column = bit.bit_length() - 1
            columns.append(column)
            if row <= reach:
                total += search(
                    row + 1,
                    usedColumns | bit,
                    ((leftDiagonals | bit) << 1) & fullMask,
                    (rightDiagonals | bit) >> 1,
                )
            else:
                total += search(row + 1, 0, 0, 0)
            columns.pop()
        return total

    total = 0
    for column, multiplier in _reflectedFirstRowStates(n).items():
        bit = 1 << column
        columns.append(column)
        total += multiplier * search(
            1,
            bit,
            (bit << 1) & fullMask,
            bit >> 1,
        )
        columns.pop()
    return total


def weakQueenCount(n, weakness):
    reach = n - 1 - weakness
    if reach == 0:
        return n ** n
    if reach == n - 1:
        return _classicalQueenCount(n)
    if reach >= n - 3:
        return _lateReleaseQueenCount(n, reach)
    return _transferQueenCount(n, reach)


def weakQueenSum(n):
    return sum(weakQueenCount(n, weakness) for weakness in range(n))


def runTests():
    assert weakQueenCount(4, 0) == 2
    assert weakQueenCount(4, 2) == 16
    assert weakQueenCount(4, 3) == 256
    assert weakQueenSum(4) == 276
    assert weakQueenSum(5) == 3_347


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = weakQueenSum(14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
