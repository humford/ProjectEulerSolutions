import math
import time


def powerOfTwoLeadingDigits(prefix, occurrence):
    digits = len(str(prefix))
    lower = math.log10(prefix) - digits + 1
    upper = math.log10(prefix + 1) - digits + 1
    step = math.log10(2)

    fraction = 0.0
    count = 0
    exponent = 0
    while count < occurrence:
        exponent += 1
        fraction += step
        if fraction >= 1.0:
            fraction -= 1.0
        if lower <= fraction < upper:
            count += 1

    return exponent


def runTests():
    assert 2 ** 7 == 128
    assert powerOfTwoLeadingDigits(12, 1) == 7
    assert powerOfTwoLeadingDigits(12, 2) == 80
    assert powerOfTwoLeadingDigits(123, 45) == 12_710


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = powerOfTwoLeadingDigits(123, 678_910)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
