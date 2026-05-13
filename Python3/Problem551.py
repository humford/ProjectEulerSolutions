from functools import lru_cache
import time


POWERS_OF_TEN = [1]
for _ in range(20):
    POWERS_OF_TEN.append(POWERS_OF_TEN[-1] * 10)


def digitSum(n):
    return sum(int(digit) for digit in str(n))


@lru_cache(None)
def crossPowerOfTen(digits, prefixDigitSum, suffix):
    threshold = POWERS_OF_TEN[digits]

    if suffix == 0 and prefixDigitSum == 0:
        raise ValueError("zero does not advance under the digit-sum recurrence")

    if digits == 0:
        return 1, prefixDigitSum - 1

    block = POWERS_OF_TEN[digits - 1]
    highDigit = suffix // block
    lower = suffix % block
    steps = 0

    while highDigit < 10:
        blockSteps, residual = crossPowerOfTen(
            digits - 1, prefixDigitSum + highDigit, lower
        )
        steps += blockSteps
        highDigit += 1 + residual // block
        lower = residual % block

    return steps, (highDigit - 10) * block + lower


def jumpToNextMultiple(value, digits):
    threshold = POWERS_OF_TEN[digits]
    prefix, suffix = divmod(value, threshold)
    steps, residual = crossPowerOfTen(digits, digitSum(prefix), suffix)
    return steps, (prefix + 1) * threshold + residual


def valueAfterSteps(steps):
    index = 0
    value = 1

    while index < steps:
        remaining = steps - index

        for digits in range(len(str(value)) + 2, 0, -1):
            try:
                jumpSteps, nextValue = jumpToNextMultiple(value, digits)
            except ValueError:
                continue

            if jumpSteps <= remaining:
                index += jumpSteps
                value = nextValue
                break
        else:
            value += digitSum(value)
            index += 1

    return value


def digitSumSequence(index):
    if index <= 1:
        return 1
    return valueAfterSteps(index - 1)


def runTests():
    assert [digitSumSequence(index) for index in range(10)] == [
        1,
        1,
        2,
        4,
        8,
        16,
        23,
        28,
        38,
        49,
    ]
    assert digitSumSequence(10) == 62
    assert digitSumSequence(10 ** 6) == 31_054_319


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = digitSumSequence(10 ** 15)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
