import time


def radicals(limit):
    values = [1] * (limit + 1)

    for n in range(2, limit + 1):
        if values[n] == 1:
            for multiple in range(n, limit + 1, n):
                values[multiple] *= n

    return values


def orderedRadicalElement(limit, index):
    values = radicals(limit)
    ordered = sorted(range(1, limit + 1), key=lambda n: (values[n], n))
    return ordered[index - 1]


def runTests():
    assert orderedRadicalElement(10, 4) == 8


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = orderedRadicalElement(100000, 10000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
