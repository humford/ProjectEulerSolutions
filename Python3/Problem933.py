from dataclasses import dataclass
import time

try:
    import numpy as np
except ImportError:
    np = None


TARGET_W = 123
TARGET_H = 1_234_567


@dataclass
class WidthState:
    grundyValues: list[int]
    stableStart: int
    stableGrundy: int
    countValues: list[int]
    tailStart: int
    tailSlope: int
    tailIntercept: int


def mexFromMask(mask):
    value = 0
    while mask & (1 << value):
        value += 1
    return value


def grundyAt(states, width, height):
    state = states[width]
    if height >= state.stableStart:
        return state.stableGrundy
    return state.grundyValues[height]


def computeFiniteValuesWithNumpy(cutSequences, tailStart):
    sequenceArray = np.array(
        [sequence for sequence, _, _, _ in cutSequences],
        dtype=np.uint16,
    )
    multiplicities = np.array(
        [multiplicity for _, multiplicity, _, _ in cutSequences],
        dtype=np.int64,
    )
    grundyValues = [0] * (tailStart + 1)
    countValues = [0] * (tailStart + 1)

    for height in range(2, tailStart + 1):
        stop = (height + 1) // 2
        left = sequenceArray[:, 1:stop]
        right = sequenceArray[:, height - 1 : height - stop : -1]
        mask = 0

        if left.size:
            xorValues = np.bitwise_xor(left, right)
            zeroCounts = np.count_nonzero(xorValues == 0, axis=1) * 2

            for value in np.unique(xorValues):
                mask |= 1 << int(value)
        else:
            zeroCounts = np.zeros(len(cutSequences), dtype=np.int64)

        if height % 2 == 0:
            mask |= 1
            zeroCounts = zeroCounts + 1

        grundyValues[height] = mexFromMask(mask)
        countValues[height] = int(np.dot(zeroCounts, multiplicities))

    return grundyValues, countValues


def computeFiniteValuesWithPython(cutSequences, tailStart):
    grundyValues = [0] * (tailStart + 1)
    countValues = [0] * (tailStart + 1)

    for height in range(2, tailStart + 1):
        mask = 0
        winningMoves = 0

        for sequence, multiplicity, _, _ in cutSequences:
            localWinningMoves = 0

            for cutHeight in range(1, (height + 1) // 2):
                xorValue = sequence[cutHeight] ^ sequence[height - cutHeight]
                if xorValue == 0:
                    localWinningMoves += 2

                mask |= 1 << xorValue

            if height % 2 == 0:
                mask |= 1
                localWinningMoves += 1

            winningMoves += multiplicity * localWinningMoves

        grundyValues[height] = mexFromMask(mask)
        countValues[height] = winningMoves

    return grundyValues, countValues


def buildWidthState(states, width):
    previousStableLimit = max(states[w].stableStart for w in range(1, width))
    tailStart = 2 * previousStableLimit
    cutSequenceMap = {}

    for leftWidth in range(1, width // 2 + 1):
        rightWidth = width - leftWidth
        multiplicity = 1 if leftWidth == rightWidth else 2
        leftState = states[leftWidth]
        rightState = states[rightWidth]
        pairStableStart = max(leftState.stableStart, rightState.stableStart)
        pairStableGrundy = leftState.stableGrundy ^ rightState.stableGrundy
        sequence = tuple(
            grundyAt(states, leftWidth, height)
            ^ grundyAt(states, rightWidth, height)
            for height in range(tailStart + 1)
        )

        if sequence in cutSequenceMap:
            currentMultiplicity, currentStart, currentGrundy = cutSequenceMap[sequence]
            assert currentGrundy == pairStableGrundy
            cutSequenceMap[sequence] = (
                currentMultiplicity + multiplicity,
                max(currentStart, pairStableStart),
                currentGrundy,
            )
        else:
            cutSequenceMap[sequence] = (
                multiplicity,
                pairStableStart,
                pairStableGrundy,
            )

    cutSequences = [
        (sequence, multiplicity, pairStableStart, pairStableGrundy)
        for sequence, (
            multiplicity,
            pairStableStart,
            pairStableGrundy,
        ) in cutSequenceMap.items()
    ]

    tailMask = 1
    tailSlope = width - 1
    tailIntercept = 0

    for sequence, multiplicity, pairStableStart, pairStableGrundy in cutSequences:
        equalEdges = 0

        for height in range(1, pairStableStart):
            tailMask |= 1 << (sequence[height] ^ pairStableGrundy)
            if sequence[height] == pairStableGrundy:
                equalEdges += 1

        tailIntercept += multiplicity * (1 - 2 * pairStableStart + 2 * equalEdges)

    tailGrundy = mexFromMask(tailMask)

    if np is None:
        grundyValues, countValues = computeFiniteValuesWithPython(
            cutSequences,
            tailStart,
        )
    else:
        grundyValues, countValues = computeFiniteValuesWithNumpy(
            cutSequences,
            tailStart,
        )

    assert grundyValues[tailStart] == tailGrundy
    assert countValues[tailStart] == tailSlope * tailStart + tailIntercept

    stableStart = tailStart
    while stableStart > 2 and grundyValues[stableStart - 1] == tailGrundy:
        stableStart -= 1

    return WidthState(
        grundyValues[:stableStart],
        stableStart,
        tailGrundy,
        countValues,
        tailStart,
        tailSlope,
        tailIntercept,
    )


def buildStates(maxWidth):
    states = {
        1: WidthState([0], 1, 0, [0], 1, 0, 0),
    }

    for width in range(2, maxWidth + 1):
        states[width] = buildWidthState(states, width)

    return states


def winningMoveSumForWidth(state, maxHeight):
    if maxHeight < 2:
        return 0

    prefixLimit = min(maxHeight, state.tailStart - 1)
    total = sum(state.countValues[2 : prefixLimit + 1])

    if maxHeight >= state.tailStart:
        count = maxHeight - state.tailStart + 1
        heightSum = (state.tailStart + maxHeight) * count // 2
        total += state.tailSlope * heightSum + state.tailIntercept * count

    return total


def D(maxWidth, maxHeight):
    states = buildStates(maxWidth)
    return sum(
        winningMoveSumForWidth(states[width], maxHeight)
        for width in range(2, maxWidth + 1)
    )


def C(width, height):
    state = buildStates(width)[width]
    if height < state.tailStart:
        return state.countValues[height]
    return state.tailSlope * height + state.tailIntercept


def solve():
    return D(TARGET_W, TARGET_H)


def runTests():
    assert C(5, 3) == 4
    assert D(12, 123) == 327_398


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
