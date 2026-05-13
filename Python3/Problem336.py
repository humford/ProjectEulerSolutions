import time


LENGTH = 11
RANK = 2011


def nextPermutation(values):
    index = len(values) - 2

    while index >= 0 and values[index] >= values[index + 1]:
        index -= 1

    if index < 0:
        return False

    swapIndex = len(values) - 1
    while values[swapIndex] <= values[index]:
        swapIndex -= 1

    values[index], values[swapIndex] = values[swapIndex], values[index]
    values[index + 1 :] = reversed(values[index + 1 :])

    return True


def simonRotations(train):
    current = list(train)
    rotations = 0

    for index in range(len(current) - 1):
        expected = chr(ord("A") + index)

        if current[index] == expected:
            return rotations

        if current[-1] == expected and index != len(current) - 2:
            return rotations

        target = index + 1
        while current[target] != expected:
            target += 1

        if target < len(current) - 1:
            current[target:] = reversed(current[target:])
            rotations += 1

        current[index:] = reversed(current[index:])
        rotations += 1

    return rotations


def maximixArrangement(length=LENGTH, rank=RANK):
    train = list("CABDEFGHIJKLM"[:length])
    maximumRotations = 2 * (length - 1) - 1
    found = 0

    while True:
        if simonRotations(train) == maximumRotations:
            found += 1

            if found == rank:
                return "".join(train)

        if not nextPermutation(train):
            raise RuntimeError("Rank not found")


def runTests():
    assert maximixArrangement(6, 10) == "DFAECB"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximixArrangement()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
