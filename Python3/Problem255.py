import decimal
import time


DIGITS = 14


def nextEstimate(number, estimate):
    return (estimate + (number + estimate - 1) // estimate) // 2


def iterationCount(number):
    digit_count = len(str(number))
    if digit_count % 2 == 0:
        estimate = 7 * 10 ** ((digit_count - 2) // 2)
    else:
        estimate = 2 * 10 ** ((digit_count - 1) // 2)

    result = 0
    while True:
        next_estimate = nextEstimate(number, estimate)
        result += 1
        if next_estimate == estimate:
            return result
        estimate = next_estimate


def initialEstimate(digit_count):
    if digit_count % 2 == 0:
        return 7 * 10 ** ((digit_count - 2) // 2)
    return 2 * 10 ** ((digit_count - 1) // 2)


def totalIterationsForRange(low, high, estimate):
    result = 0
    first_next = (estimate + (low + estimate - 1) // estimate) // 2
    last_next = (estimate + (high + estimate - 1) // estimate) // 2

    for next_estimate in range(first_next, last_next + 1):
        ceil_low = 2 * next_estimate - estimate
        ceil_high = ceil_low + 1
        sub_low = (ceil_low - 1) * estimate + 1
        sub_high = ceil_high * estimate

        if sub_low < low:
            sub_low = low
        if sub_high > high:
            sub_high = high
        if sub_low > sub_high:
            continue

        count = sub_high - sub_low + 1
        if next_estimate == estimate:
            result += count
        else:
            result += count + totalIterationsForRange(
                sub_low, sub_high, next_estimate
            )

    return result


def averageIterations(digit_count):
    low = 10 ** (digit_count - 1)
    high = 10**digit_count - 1
    total = totalIterationsForRange(low, high, initialEstimate(digit_count))
    count = high - low + 1
    decimal.getcontext().prec = 40
    return decimal.Decimal(total) / decimal.Decimal(count)


def roundedAverageIterations(digit_count):
    average = averageIterations(digit_count)
    rounded = average.quantize(decimal.Decimal("0.0000000001"))
    return format(rounded, ".10f")


def runTests():
    assert iterationCount(4321) == 2
    assert roundedAverageIterations(5) == "3.2102888889"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedAverageIterations(DIGITS)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
