import time


def tValues(limit):
    value = 290797
    result = []

    for _ in range(limit + 1):
        result.append(value % 64 + 1)
        value = value * value % 50515093

    return result


def expandRuns(runs):
    bits = []
    occupied = 1

    for run in runs:
        bits.extend([occupied] * run)
        occupied ^= 1

    return bits


def bbsTurn(bits):
    ballPositions = [index for index, bit in enumerate(bits) if bit]
    bits = bits + [0] * (len(ballPositions) + 100)
    empty = 0

    for position in ballPositions:
        if empty <= position:
            empty = position + 1

        while bits[empty]:
            empty += 1

        bits[position] = 0
        bits[empty] = 1

    while bits and bits[-1] == 0:
        bits.pop()

    return bits


def occupiedBlocks(bits):
    blocks = []
    index = 0

    while index < len(bits):
        if bits[index]:
            end = index

            while end < len(bits) and bits[end]:
                end += 1

            blocks.append(end - index)
            index = end
        else:
            index += 1

    return blocks


def smallFinalState(runs):
    bits = expandRuns(runs)
    previous = None
    stable = 0

    while stable <= 20:
        bits = bbsTurn(bits)
        blocks = occupiedBlocks(bits)

        if blocks == previous:
            stable += 1
        else:
            stable = 0
            previous = blocks

    return previous


def eliminationCounts(runs):
    counts = [0]
    stack = []

    for index, run in enumerate(runs):
        if index % 2 == 0:
            stack.extend([0] * run)
            continue

        for _ in range(min(run, len(stack))):
            level = stack.pop() + 1
            if level >= len(counts):
                counts.extend([0] * (level - len(counts) + 1))
            counts[level] += 1

            if stack and stack[-1] < level:
                stack[-1] = level

    while stack:
        level = stack.pop() + 1
        if level >= len(counts):
            counts.extend([0] * (level - len(counts) + 1))
        counts[level] += 1

        if stack and stack[-1] < level:
            stack[-1] = level

    return counts


def finalState(runs):
    counts = eliminationCounts(runs)
    counts.append(0)
    state = []

    for length in range(1, len(counts) - 1):
        state.extend([length] * (counts[length] - counts[length + 1]))

    return state


def finalSquareSum(limit=10_000_000):
    counts = eliminationCounts(tValues(limit))
    return sum((2 * level - 1) * count for level, count in enumerate(counts))


def runTests():
    assert smallFinalState((2, 2, 2, 1, 2)) == [1, 2, 3]
    assert finalState((2, 2, 2, 1, 2)) == [1, 2, 3]
    assert finalState(tValues(10)) == [1, 3, 10, 24, 51, 75]
    assert finalSquareSum(10) == 8912


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = finalSquareSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
