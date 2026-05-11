def firstFibonacciTermWithDigits(digits):
    previous = 1
    current = 1
    index = 2
    threshold = 10 ** (digits - 1)

    while current < threshold:
        previous, current = current, previous + current
        index += 1

    return index


def runTests():
    assert firstFibonacciTermWithDigits(3) == 12


def solve():
    return firstFibonacciTermWithDigits(1000)


if __name__ == "__main__":
    runTests()
    print(solve())
