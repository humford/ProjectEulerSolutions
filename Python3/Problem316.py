import time


LIMIT = 10**16
MAX_DIVISOR = 999999


def expectedPosition(number):
    digits = str(number)
    length = len(digits)
    total = 10**length - length + 1

    for borderLength in range(1, length):
        if digits[:borderLength] == digits[-borderLength:]:
            total += 10**borderLength

    return total


def expectedPositionSum(limit, maxDivisor):
    total = 0

    for divisor in range(2, maxDivisor + 1):
        total += expectedPosition(limit // divisor)

    return total


def runTests():
    assert expectedPosition(535) == 1008
    assert expectedPositionSum(10**6, 999) == 27280188


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedPositionSum(LIMIT, MAX_DIVISOR)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
