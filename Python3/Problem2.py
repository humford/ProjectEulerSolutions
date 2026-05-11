def sumEvenFibonacci(maxVal):
    total = 0
    previous = 1
    current = 2

    while current <= maxVal:
        if current % 2 == 0:
            total += current
        previous, current = current, previous + current

    return total


def runTests():
    assert sumEvenFibonacci(89) == 44


def solve():
    return sumEvenFibonacci(4000000)


if __name__ == "__main__":
    runTests()
    print(solve())
