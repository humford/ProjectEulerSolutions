import time


def sumAlmostEquilateralPerimeters(limit):
    total = 0
    x = 2
    y = 0

    while True:
        x, y = 2 * x + 3 * y, x + 2 * y

        if x % 3 == 2:
            perimeter = x + 2
        elif x % 3 == 1:
            perimeter = x - 2
        else:
            continue

        if perimeter > limit:
            return total
        if perimeter > 2:
            total += perimeter


def runTests():
    assert sumAlmostEquilateralPerimeters(1000) == 984


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumAlmostEquilateralPerimeters(1000000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
