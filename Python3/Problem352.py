import time


SHEEP = 10000
MAX_POOL_SIZE = 100


def round6(value):
    return float("{:.6f}".format(value))


def expectedTests(sheep, probability, maxPoolSize=MAX_POOL_SIZE):
    maxPoolSize = min(maxPoolSize, sheep)
    healthyProbability = 1.0 - probability
    powers = [1.0] * (maxPoolSize + 1)

    for size in range(1, maxPoolSize + 1):
        powers[size] = powers[size - 1] * healthyProbability

    unconditional = [0.0] * (sheep + 1)
    positive = [0.0] * (maxPoolSize + 1)

    if sheep >= 1:
        unconditional[1] = 1.0

    limit = min(sheep, maxPoolSize)

    for size in range(2, limit + 1):
        denominator = 1.0 - powers[size]
        bestPositive = float("inf")

        for poolSize in range(1, size):
            positiveProbability = (1.0 - powers[poolSize]) / denominator
            candidate = (
                1.0
                + positiveProbability
                * (positive[poolSize] + unconditional[size - poolSize])
                + (1.0 - positiveProbability) * positive[size - poolSize]
            )

            if candidate < bestPositive:
                bestPositive = candidate

        positive[size] = bestPositive
        bestUnconditional = float("inf")

        for poolSize in range(1, size + 1):
            candidate = (
                1.0
                + unconditional[size - poolSize]
                + (1.0 - powers[poolSize]) * positive[poolSize]
            )

            if candidate < bestUnconditional:
                bestUnconditional = candidate

        unconditional[size] = bestUnconditional

    for size in range(limit + 1, sheep + 1):
        bestUnconditional = float("inf")

        for poolSize in range(1, maxPoolSize + 1):
            candidate = (
                1.0
                + unconditional[size - poolSize]
                + (1.0 - powers[poolSize]) * positive[poolSize]
            )

            if candidate < bestUnconditional:
                bestUnconditional = candidate

        unconditional[size] = bestUnconditional

    return unconditional[sheep]


def bloodTestSum():
    return sum(expectedTests(SHEEP, probability / 100.0) for probability in range(1, 51))


def runTests():
    assert round6(expectedTests(25, 0.02)) == 4.155452
    assert round6(expectedTests(25, 0.10)) == 12.702124


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.6f}".format(bloodTestSum())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
