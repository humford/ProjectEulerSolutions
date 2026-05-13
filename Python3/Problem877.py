import time


TARGET_N = 10**18


def xorProduct(a, b):
    product = 0

    while b:
        if b & 1:
            product ^= a
        a <<= 1
        b >>= 1

    return product


def isSolution(a, b):
    return (
        xorProduct(a, a)
        ^ xorProduct(2, xorProduct(a, b))
        ^ xorProduct(b, b)
    ) == 5


def solutionBValues(limit):
    previous = 0
    current = 3
    values = []

    while current <= limit:
        values.append(current)
        previous, current = current, (current << 1) ^ previous

    return values


def X(limit):
    total = 0
    for value in solutionBValues(limit):
        total ^= value
    return total


def bruteX(limit):
    total = 0

    for a in range(limit + 1):
        for b in range(a, limit + 1):
            if isSolution(a, b):
                total ^= b

    return total


def runTests():
    assert xorProduct(7, 3) == 9
    assert isSolution(3, 6)
    assert solutionBValues(10) == [3, 6]
    assert X(10) == 5
    assert X(100) == bruteX(100)


def solve():
    return X(TARGET_N)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
