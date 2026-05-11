def sumMultiples(first, second, limit):
    total = 0
    for value in range(limit):
        if value % first == 0 or value % second == 0:
            total += value
    return total


def runTests():
    assert sumMultiples(3, 5, 10) == 23


def solve():
    return sumMultiples(3, 5, 1000)


if __name__ == "__main__":
    runTests()
    print(solve())
