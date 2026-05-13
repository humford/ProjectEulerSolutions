import time
from functools import lru_cache


MODULUS = 10**18


def valueFromDigits(digits, base):
    value = 0

    for digit in digits:
        value = value * base + digit

    return value


def digitsInBase(number, base):
    digits = []

    for _ in range(5):
        digits.append(number % base)
        number //= base

    return list(reversed(digits))


def kaprekarStep(number, base):
    digits = digitsInBase(number, base)

    return valueFromDigits(sorted(digits, reverse=True), base) - valueFromDigits(
        sorted(digits),
        base,
    )


def kaprekarConstant(base):
    parameter = (base - 3) // 6
    digits = (
        4 * parameter + 2,
        2 * parameter,
        6 * parameter + 2,
        4 * parameter + 1,
        2 * parameter + 1,
    )

    return valueFromDigits(digits, base)


def kaprekarConstantState(base):
    parameter = (base - 3) // 6

    return 4 * parameter + 2, 2 * parameter + 1


def kaprekarState(number, base):
    digits = sorted(digitsInBase(number, base))

    return digits[-1] - digits[0], digits[-2] - digits[1]


def nextState(state, base):
    highGap, middleGap = state

    if middleGap == 0:
        lowDigit = highGap - 1
        otherLowDigit = base - highGap

        if lowDigit <= otherLowDigit:
            return base - 1 - lowDigit, base - 1 - otherLowDigit

        return base - 1 - otherLowDigit, base - 1 - lowDigit

    digits = (
        highGap,
        middleGap - 1,
        base - 1,
        base - middleGap - 1,
        base - highGap,
    )
    sortedDigits = sorted(digits)

    return sortedDigits[-1] - sortedDigits[0], sortedDigits[-2] - sortedDigits[1]


def stateMultiplicity(highGap, middleGap, base):
    shiftedMinimumChoices = base - highGap

    if middleGap == 0:
        perShift = 20 * highGap - 10
    elif middleGap == highGap:
        perShift = 30 * highGap - 10
    else:
        perShift = 120 * middleGap * (highGap - middleGap) - 20

    return shiftedMinimumChoices * perShift


def kaprekarSum(base):
    targetState = kaprekarConstantState(base)

    @lru_cache(maxsize=None)
    def stepsFromState(state):
        if state == targetState:
            return 1

        return 1 + stepsFromState(nextState(state, base))

    total = 0

    for highGap in range(1, base):
        for middleGap in range(highGap + 1):
            state = highGap, middleGap
            total += stateMultiplicity(highGap, middleGap, base) * stepsFromState(state)

    return total - 1


def finalSuffix():
    total = 0

    for multiplier in range(2, 301):
        total += kaprekarSum(6 * multiplier + 3)

    return total % MODULUS


def runTests():
    assert digitsInBase(kaprekarConstant(15), 15) == [10, 4, 14, 9, 5]
    assert digitsInBase(kaprekarConstant(21), 21) == [14, 6, 20, 13, 7]
    assert kaprekarStep(kaprekarConstant(15), 15) == kaprekarConstant(15)
    assert kaprekarState(kaprekarConstant(15), 15) == kaprekarConstantState(15)
    assert kaprekarSum(15) == 5274369
    assert kaprekarSum(111) == 400668930299


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = finalSuffix()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
