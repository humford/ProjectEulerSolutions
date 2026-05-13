import math
import time


def inverseBranch(value, branch):
    root = math.hypot(value, 2.0)
    if branch == 0:
        return 0.5 * (value + root)
    return 0.5 * (value - root)


def orbitRange(branches):
    x = 0.0
    for _ in range(12):
        y = x
        for branch in branches:
            y = inverseBranch(y, branch)
        if abs(y - x) <= 1e-16 * (1.0 + abs(y)):
            x = y
            break
        x = y

    y = x
    minimum = y
    maximum = y
    for branch in branches[:-1]:
        y = inverseBranch(y, branch)
        if y < minimum:
            minimum = y
        if y > maximum:
            maximum = y

    return maximum - minimum


def forEachAperiodicBinaryNecklace(length, callback):
    word = [0] * (length + 1)

    def search(index, period):
        if index > length:
            if period == length:
                callback(word[1:])
            return

        word[index] = word[index - period]
        search(index + 1, period)

        if word[index - period] == 0:
            word[index] = 1
            search(index + 1, index)

    search(1, 1)


def periodicSequenceRangeSum(periodLimit):
    if periodLimit < 2:
        return 0.0

    total = 0.0
    chunk = []

    def flush():
        nonlocal total
        if chunk:
            total += math.fsum(chunk)
            chunk.clear()

    for length in range(2, periodLimit + 1):
        def handle(branches):
            chunk.append(length * orbitRange(branches))
            if len(chunk) >= 50_000:
                flush()

        forEachAperiodicBinaryNecklace(length, handle)
        flush()

    return total


def runTests():
    assert format(periodicSequenceRangeSum(2), ".4f") == "2.8284"
    assert format(periodicSequenceRangeSum(3), ".4f") == "14.6461"
    assert format(periodicSequenceRangeSum(5), ".4f") == "124.1056"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(periodicSequenceRangeSum(25), ".4f")
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
