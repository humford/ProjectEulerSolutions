import time


def digitalRoot(n):
    return 1 + (n - 1) % 9


def maximumDigitalRootSums(limit):
    values = bytearray(digitalRoot(n) for n in range(limit))

    for factor in range(2, limit):
        factor_value = values[factor]
        for multiple in range(2 * factor, limit, factor):
            candidate = factor_value + values[multiple // factor]
            if candidate > values[multiple]:
                values[multiple] = candidate

    return values


def mdrsSum(limit):
    return sum(maximumDigitalRootSums(limit)[2:])


def runTests():
    values = maximumDigitalRootSums(25)
    assert values[24] == 11


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = mdrsSum(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
