import time


def fibonacciNumbers(count):
    values = [0, 1]
    while len(values) <= count:
        values.append(values[-1] + values[-2])
    return values


def goldenNuggets(count):
    fibs = fibonacciNumbers(2 * count + 1)
    return [fibs[2 * index] * fibs[2 * index + 1] for index in range(1, count + 1)]


def runTests():
    assert goldenNuggets(5) == [2, 15, 104, 714, 4895]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = goldenNuggets(15)[-1]
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
