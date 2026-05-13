import math
import time


INITIAL_EXACT_DIGITS = 6
MOMENTS = 8
TAIL_TOLERANCE = 1e-15


def hasThreeConsecutiveEqualDigits(number):
    text = str(number)

    return any(text[index] == text[index + 1] == text[index + 2] for index in range(len(text) - 2))


def omittedDenominators(limit):
    return [number for number in range(1, limit + 1) if hasThreeConsecutiveEqualDigits(number)]


def isAllowedText(text):
    return not any(text[index] == text[index + 1] == text[index + 2] for index in range(len(text) - 2))


def suffixState(text):
    lastDigit = text[-1]
    runLength = 1

    for digit in reversed(text[:-1]):
        if digit != lastDigit:
            break
        runLength += 1

    return int(lastDigit), min(runLength, 2)


def emptyStateSums(moments):
    return {(digit, runLength): [0.0] * (moments + 1) for digit in range(10) for runLength in (1, 2)}


def initialStateSums(exactDigits, moments):
    stateSums = emptyStateSums(moments)
    total = 0.0

    for length in range(1, exactDigits + 1):
        for number in range(10 ** (length - 1), 10 ** length):
            text = str(number)
            if not isAllowedText(text):
                continue

            if length < exactDigits:
                total += 1.0 / number
                continue

            inverse = 1.0 / number
            inversePower = inverse
            sums = stateSums[suffixState(text)]
            for power in range(1, moments + 1):
                sums[power] += inversePower
                inversePower *= inverse

    return total, stateSums


def transitionCoefficients(moments):
    coefficients = {}

    for digit in range(10):
        for power in range(1, moments + 1):
            entries = []
            for extraPower in range(moments - power + 1):
                sign = -1 if extraPower % 2 else 1
                coefficient = sign * math.comb(power + extraPower - 1, extraPower)
                coefficient *= digit ** extraPower
                coefficient *= 10.0 ** (-(power + extraPower))
                entries.append((power + extraPower, coefficient))
            coefficients[(digit, power)] = entries

    return coefficients


def advanceStateSums(stateSums, moments, coefficients):
    nextStateSums = emptyStateSums(moments)

    for (lastDigit, runLength), sums in stateSums.items():
        for digit in range(10):
            if digit == lastDigit and runLength == 2:
                continue

            nextRunLength = runLength + 1 if digit == lastDigit else 1
            nextSums = nextStateSums[(digit, nextRunLength)]

            for power in range(1, moments + 1):
                value = 0.0
                for sourcePower, coefficient in coefficients[(digit, power)]:
                    value += coefficient * sums[sourcePower]
                nextSums[power] += value

    return nextStateSums


def kempnerLikeSeries(tolerance=TAIL_TOLERANCE, exactDigits=INITIAL_EXACT_DIGITS, moments=MOMENTS):
    total, stateSums = initialStateSums(exactDigits, moments)
    total += sum(sums[1] for sums in stateSums.values())
    coefficients = transitionCoefficients(moments)

    while True:
        stateSums = advanceStateSums(stateSums, moments, coefficients)
        contribution = sum(sums[1] for sums in stateSums.values())
        total += contribution

        if contribution < tolerance:
            return total


def formattedAnswer():
    return format(kempnerLikeSeries(), ".10f")


def runTests():
    omitted = omittedDenominators(1200)
    assert len(omitted) == 20
    assert omitted == [
        111,
        222,
        333,
        444,
        555,
        666,
        777,
        888,
        999,
        1000,
        1110,
        1111,
        1112,
        1113,
        1114,
        1115,
        1116,
        1117,
        1118,
        1119,
    ]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedAnswer()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
