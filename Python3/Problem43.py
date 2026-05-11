from itertools import permutations


DIVISORS = (2, 3, 5, 7, 11, 13, 17)


def hasSubStringDivisibility(digits):
    text = "".join(digits)
    return all(int(text[index:index + 3]) % divisor == 0 for index, divisor in enumerate(DIVISORS, start=1))


def subStringDivisiblePandigitals():
    return [
        int("".join(permutation))
        for permutation in permutations("0123456789")
        if hasSubStringDivisibility(permutation)
    ]


def runTests():
    assert hasSubStringDivisibility("1406357289")


def solve():
    return sum(subStringDivisiblePandigitals())


if __name__ == "__main__":
    runTests()
    print(solve())
