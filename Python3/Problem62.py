def smallestCubicPermutation(targetCount):
    root = 1
    digits = 1

    while True:
        groups = {}
        while len(str(root ** 3)) == digits:
            cube = root ** 3
            key = "".join(sorted(str(cube)))
            groups.setdefault(key, []).append(cube)
            root += 1

        candidates = [min(cubes) for cubes in groups.values() if len(cubes) == targetCount]
        if candidates:
            return min(candidates)

        digits += 1


def runTests():
    assert smallestCubicPermutation(3) == 41063625


def solve():
    return smallestCubicPermutation(5)


if __name__ == "__main__":
    runTests()
    print(solve())
