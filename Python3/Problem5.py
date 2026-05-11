from math import gcd


def leastCommonMultiple(first, second):
    return first * second // gcd(first, second)


def smallestMultiple(limit):
    result = 1
    for value in range(2, limit + 1):
        result = leastCommonMultiple(result, value)
    return result


def runTests():
    assert smallestMultiple(10) == 2520


def solve():
    return smallestMultiple(20)


if __name__ == "__main__":
    runTests()
    print(solve())
