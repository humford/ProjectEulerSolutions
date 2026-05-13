from functools import lru_cache
import time


MODULUS = 1_000_000_007
INVERSE_TWO = (MODULUS + 1) // 2


def signedDifferenceDirect(width, height):
    if height <= 0:
        return 0

    dp = [MODULUS - 1 if index % 2 == 0 else 1 for index in range(height)]

    for _ in range(2, width + 1):
        total = sum(dp) % MODULUS
        normalPrefix = 0
        alternatingPrefix = 0
        sign = -1
        nextDp = [0] * height

        for index, value in enumerate(dp):
            if sign == -1:
                nextDp[index] = (total - normalPrefix - alternatingPrefix) % MODULUS
            else:
                nextDp[index] = (total - normalPrefix + alternatingPrefix) % MODULUS

            normalPrefix += value
            alternatingPrefix += sign * value
            sign = -sign

        dp = nextDp

    return sum(dp) % MODULUS


def signedDifferenceExact(width, height):
    if height <= 0:
        return 0

    dp = [-1 if index % 2 == 0 else 1 for index in range(height)]

    for _ in range(2, width + 1):
        total = sum(dp)
        normalPrefix = 0
        alternatingPrefix = 0
        sign = -1
        nextDp = [0] * height

        for index, value in enumerate(dp):
            nextDp[index] = total - normalPrefix + sign * alternatingPrefix
            normalPrefix += value
            alternatingPrefix += sign * value
            sign = -sign

        dp = nextDp

    return sum(dp)


def berlekampMassey(sequence):
    correction = [1]
    previous = [1]
    order = 0
    shift = 1
    lastDiscrepancy = 1

    for index in range(len(sequence)):
        discrepancy = sequence[index]
        for term in range(1, order + 1):
            discrepancy = (discrepancy + correction[term] * sequence[index - term]) % MODULUS

        if discrepancy == 0:
            shift += 1
            continue

        oldCorrection = correction[:]
        scale = discrepancy * pow(lastDiscrepancy, MODULUS - 2, MODULUS) % MODULUS

        if len(correction) < len(previous) + shift:
            correction.extend([0] * (len(previous) + shift - len(correction)))

        for term, value in enumerate(previous):
            correction[term + shift] = (correction[term + shift] - scale * value) % MODULUS

        if 2 * order <= index:
            order = index + 1 - order
            previous = oldCorrection
            lastDiscrepancy = discrepancy
            shift = 1
        else:
            shift += 1

    return [(-correction[index]) % MODULUS for index in range(1, order + 1)]


def combinePolynomials(left, right, recurrence):
    degree = len(recurrence)
    result = [0] * (2 * degree - 1)

    for leftIndex, leftValue in enumerate(left):
        if leftValue == 0:
            continue

        for rightIndex, rightValue in enumerate(right):
            if rightValue:
                result[leftIndex + rightIndex] = (
                    result[leftIndex + rightIndex] + leftValue * rightValue
                ) % MODULUS

    for index in range(2 * degree - 2, degree - 1, -1):
        value = result[index]
        if value == 0:
            continue

        for offset, coefficient in enumerate(recurrence, 1):
            result[index - offset] = (result[index - offset] + value * coefficient) % MODULUS

    return result[:degree]


def linearRecurrenceValue(initial, recurrence, index):
    if index < len(initial):
        return initial[index] % MODULUS

    degree = len(recurrence)
    coefficients = [1] + [0] * (degree - 1)

    if degree == 1:
        power = [recurrence[0]]
    else:
        power = [0] * degree
        power[1] = 1

    while index:
        if index & 1:
            coefficients = combinePolynomials(coefficients, power, recurrence)

        power = combinePolynomials(power, power, recurrence)
        index //= 2

    return sum(coefficients[i] * initial[i] for i in range(degree)) % MODULUS


def signedDifferenceByWidthRecurrence(width, height):
    dp = [MODULUS - 1 if index % 2 == 0 else 1 for index in range(height)]
    terms = []

    for _ in range(2 * height + 5):
        terms.append(sum(dp) % MODULUS)
        total = sum(dp) % MODULUS
        normalPrefix = 0
        alternatingPrefix = 0
        sign = -1
        nextDp = [0] * height

        for index, value in enumerate(dp):
            if sign == -1:
                nextDp[index] = (total - normalPrefix - alternatingPrefix) % MODULUS
            else:
                nextDp[index] = (total - normalPrefix + alternatingPrefix) % MODULUS

            normalPrefix += value
            alternatingPrefix += sign * value
            sign = -sign

        dp = nextDp

    recurrence = berlekampMassey(terms)
    return linearRecurrenceValue(terms, recurrence, width - 1)


def interpolate(points, values, target):
    total = 0

    for index, point in enumerate(points):
        numerator = 1
        denominator = 1

        for otherIndex, otherPoint in enumerate(points):
            if index == otherIndex:
                continue

            numerator = numerator * (target - otherPoint) % MODULUS
            denominator = denominator * (point - otherPoint) % MODULUS

        total += values[index] * numerator * pow(denominator, MODULUS - 2, MODULUS)
        total %= MODULUS

    return total


def signedDifferenceByHeightInterpolation(width, height):
    if height % 2 == 0:
        target = height // 2
        sampleHeights = [2 * point for point in range(1, width + 2)]
    else:
        target = (height + 1) // 2
        sampleHeights = [2 * point - 1 for point in range(1, width + 2)]

    points = list(range(1, width + 2))
    values = [signedDifferenceDirect(width, sampleHeight) for sampleHeight in sampleHeights]
    return interpolate(points, values, target % MODULUS)


@lru_cache(maxsize=None)
def signedDifference(width, height):
    if height <= 0:
        return 0

    if height <= 200 and width > 1_000:
        return signedDifferenceByWidthRecurrence(width, height)

    if width <= 200 and height > 500:
        return signedDifferenceByHeightInterpolation(width, height)

    return signedDifferenceDirect(width, height)


def castleCountMod(width, height):
    totalSequences = (pow(height % MODULUS, width, MODULUS) - pow((height - 1) % MODULUS, width, MODULUS)) % MODULUS
    signedSequences = (signedDifference(width, height) - signedDifference(width, height - 1)) % MODULUS
    return (totalSequences + signedSequences) * INVERSE_TWO % MODULUS


def castleCountExact(width, height):
    totalSequences = height**width - (height - 1) ** width
    signedSequences = signedDifferenceExact(width, height) - signedDifferenceExact(width, height - 1)
    return (totalSequences + signedSequences) // 2


def targetCastleSum():
    return (
        castleCountMod(10**12, 100)
        + castleCountMod(10_000, 10_000)
        + castleCountMod(100, 10**12)
    ) % MODULUS


def runTests():
    assert castleCountExact(4, 2) == 10
    assert castleCountExact(13, 10) == 3_729_050_610_636
    assert castleCountExact(10, 13) == 37_959_702_514
    assert castleCountMod(100, 100) == 841_913_936


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = targetCastleSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
