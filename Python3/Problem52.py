def arePermutations(first, second):
    return sorted(str(first)) == sorted(str(second))


def smallestPermutedMultiple(maxMultiplier):
    value = 1
    while True:
        if all(arePermutations(value, value * multiplier) for multiplier in range(2, maxMultiplier + 1)):
            return value
        value += 1


def runTests():
    assert arePermutations(125874, 251748)


def solve():
    return smallestPermutedMultiple(6)


if __name__ == "__main__":
    runTests()
    print(solve())
