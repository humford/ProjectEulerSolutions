import math
import time


PATTERN = "1234567890"


def matchesPattern(square):
    digits = str(square)
    return len(digits) == 19 and digits[::2] == PATTERN


def concealedSquareRoot():
    lower = math.isqrt(1020304050607080900)
    upper = math.isqrt(1929394959697989990) + 1

    start = lower - (lower % 100) + 30
    if start < lower:
        start += 40

    candidate = start
    step = 40
    while candidate <= upper:
        if matchesPattern(candidate * candidate):
            return candidate

        candidate += step
        step = 100 - step

    return None


def runTests():
    assert matchesPattern(1020304050607080900)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = concealedSquareRoot()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
