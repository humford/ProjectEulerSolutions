from math import factorial


def lexicographicPermutation(digits, position):
    remaining = list(digits)
    index = position - 1
    output = []

    for place in range(len(remaining) - 1, -1, -1):
        block_size = factorial(place)
        selected = index // block_size
        index %= block_size
        output.append(remaining.pop(selected))

    return "".join(output)


def runTests():
    assert lexicographicPermutation("012", 4) == "120"


def solve():
    return lexicographicPermutation("0123456789", 1000000)


if __name__ == "__main__":
    runTests()
    print(solve())
