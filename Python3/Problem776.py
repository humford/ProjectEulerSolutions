import time
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


def sumsByDigitSumUpTo(limit):
    digits = [int(digit) for digit in str(limit)]
    maxSum = 9 * len(digits)

    tightCounts = [0] * (maxSum + 1)
    tightSums = [0] * (maxSum + 1)
    looseCounts = [0] * (maxSum + 1)
    looseSums = [0] * (maxSum + 1)
    tightCounts[0] = 1

    for limitDigit in digits:
        nextTightCounts = [0] * (maxSum + 1)
        nextTightSums = [0] * (maxSum + 1)
        nextLooseCounts = [0] * (maxSum + 1)
        nextLooseSums = [0] * (maxSum + 1)

        for digitSum, count in enumerate(looseCounts):
            if not count:
                continue
            shiftedSum = 10 * looseSums[digitSum]
            for digit in range(10):
                newSum = digitSum + digit
                nextLooseCounts[newSum] += count
                nextLooseSums[newSum] += shiftedSum + count * digit

        for digitSum, count in enumerate(tightCounts):
            if not count:
                continue
            shiftedSum = 10 * tightSums[digitSum]
            for digit in range(limitDigit + 1):
                newSum = digitSum + digit
                if digit == limitDigit:
                    nextTightCounts[newSum] += count
                    nextTightSums[newSum] += shiftedSum + count * digit
                else:
                    nextLooseCounts[newSum] += count
                    nextLooseSums[newSum] += shiftedSum + count * digit

        tightCounts, tightSums = nextTightCounts, nextTightSums
        looseCounts, looseSums = nextLooseCounts, nextLooseSums

    return [tightSums[i] + looseSums[i] for i in range(maxSum + 1)]


def FExact(limit):
    total = Fraction(0, 1)
    for digitSum, valueSum in enumerate(sumsByDigitSumUpTo(limit)):
        if digitSum and valueSum:
            total += Fraction(valueSum, digitSum)
    return total


def FDecimal(limit, precision=120):
    getcontext().prec = precision
    getcontext().rounding = ROUND_HALF_UP
    total = Decimal(0)
    for digitSum, valueSum in enumerate(sumsByDigitSumUpTo(limit)):
        if digitSum and valueSum:
            total += Decimal(valueSum) / Decimal(digitSum)
    return total


def formatScientific(value):
    mantissa, exponent = format(value, ".12E").split("E")
    return mantissa + "e" + str(int(exponent))


def runTests():
    assert FExact(10) == 19
    assert formatScientific(FDecimal(123)) == "1.187764610390e3"
    assert formatScientific(FDecimal(12_345)) == "4.855801996238e6"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formatScientific(FDecimal(1_234_567_890_123_456_789))
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
