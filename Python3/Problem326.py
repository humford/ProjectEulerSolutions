import time


LIMIT = 10**12
MODULUS = 10**6


def moduloSummationCount(limit=LIMIT, modulus=MODULUS):
    period = 6 * modulus
    fullPeriods = (limit + 1) // period
    remainder = (limit + 1) % period

    periodCounts = [0] * modulus
    remainderCounts = [0] * modulus
    weightedSum = 0
    prefix = 0

    periodCounts[0] = 1
    if remainder > 0:
        remainderCounts[0] = 1

    for index in range(1, period):
        value = 1 if index == 1 else weightedSum % index
        weightedSum += index * value
        prefix = (prefix + value) % modulus

        periodCounts[prefix] += 1

        if index < remainder:
            remainderCounts[prefix] += 1

    total = 0

    for periodCount, remainderCount in zip(periodCounts, remainderCounts):
        count = periodCount * fullPeriods + remainderCount
        total += count * (count - 1) // 2

    return total


def runTests():
    assert moduloSummationCount(10, 10) == 4
    assert moduloSummationCount(10**4, 10**3) == 97158


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = moduloSummationCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
