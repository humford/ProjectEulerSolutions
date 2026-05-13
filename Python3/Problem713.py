import time


def guaranteedTries(fuses, working):
    if not 2 <= working <= fuses:
        raise ValueError("require 2 <= working <= fuses")

    parts = working - 1
    size, largerParts = divmod(fuses, parts)
    return parts * size * (size - 1) // 2 + largerParts * size


def waterHeatingSum(fuses):
    if fuses < 2:
        return 0

    total = 0
    k = 1
    last = fuses - 1

    while k <= last:
        quotient = fuses // k
        kMax = min(last, fuses // quotient)
        count = kMax - k + 1
        sumK = (k + kMax) * count // 2

        total += count * fuses * quotient - (quotient * (quotient + 1) // 2) * sumK
        k = kMax + 1

    return total


def runTests():
    assert guaranteedTries(3, 2) == 3
    assert guaranteedTries(8, 4) == 7
    assert waterHeatingSum(10 ** 3) == 3_281_346


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = waterHeatingSum(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
