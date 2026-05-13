import time


TARGET = -600000000000


def arithmeticGeometricSum(r, terms):
    total = 0.0
    power = 1.0

    for k in range(1, terms + 1):
        total += (900 - 3 * k) * power
        power *= r

    return total


def root():
    low = 1.0
    high = 1.01

    for _ in range(100):
        middle = (low + high) / 2
        if arithmeticGeometricSum(middle, 5000) > TARGET:
            low = middle
        else:
            high = middle

    return (low + high) / 2


def runTests():
    assert arithmeticGeometricSum(1, 10) == 8835


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f"{root():.12f}"
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
