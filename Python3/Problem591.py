import time
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, getcontext
from math import isqrt


def decimalFraction(value):
    return value - value.to_integral_value(rounding=ROUND_FLOOR)


def decimalCeiling(value):
    return int(value.to_integral_value(rounding=ROUND_CEILING))


def nearestInteger(value):
    return int(value.to_integral_value(rounding=ROUND_HALF_EVEN))


def chudnovskyPi(digits):
    getcontext().prec = digits + 30

    constant = Decimal(426880) * Decimal(10005).sqrt()
    terms = digits // 14 + 3
    multiplier = 1
    linear = 13_591_409
    exponential = 1
    kValue = 6
    series = Decimal(linear)

    for term in range(1, terms):
        multiplier = multiplier * (kValue * kValue * kValue - 16 * kValue) // (term * term * term)
        linear += 545_140_134
        exponential *= -262_537_412_640_768_000
        series += Decimal(multiplier * linear) / Decimal(exponential)
        kValue += 12

    pi = constant / series
    getcontext().prec = digits
    return +pi


def isSquare(number):
    root = isqrt(number)
    return root * root == number


def sqrtContinuedFractionPeriod(number):
    first = isqrt(number)
    if first * first == number:
        raise ValueError("number must be nonsquare")

    mValue = 0
    dValue = 1
    term = first
    period = []
    while True:
        mValue = dValue * term - mValue
        dValue = (number - mValue * mValue) // dValue
        term = (first + mValue) // dValue
        period.append(term)
        if term == 2 * first:
            break
    return first, period


def bestPositiveMultiplier(alpha, beta, bound, period):
    if bound <= 0:
        return 0

    partialQuotients = [0]
    denominators = [1]
    previousDenominator = 0

    deltas = [alpha]
    previousDelta = Decimal(1)

    index = 1
    extraTerms = 6
    while True:
        quotient = period[(index - 1) % len(period)]
        partialQuotients.append(quotient)

        denominator = quotient * denominators[index - 1] + previousDenominator
        previousDenominator = denominators[index - 1]
        denominators.append(denominator)

        if index == 1:
            delta = -Decimal(quotient) * deltas[0] + previousDelta
        else:
            delta = -Decimal(quotient) * deltas[index - 1] + deltas[index - 2]
        deltas.append(delta)

        if denominator > bound:
            extraTerms -= 1
            if extraTerms <= 0:
                break

        index += 1

    digitCount = len(partialQuotients) - 1
    digits = [0]
    remainder = beta
    for index in range(1, digitCount + 1):
        digit = decimalCeiling(remainder / deltas[index - 1])
        digit = max(0, min(digit, partialQuotients[index]))
        digits.append(digit)
        remainder = Decimal(digit) * deltas[index - 1] - remainder

    prefixes = [0]
    total = 0
    for index in range(1, len(digits)):
        total += digits[index] * denominators[index - 1]
        prefixes.append(total)

    rightCandidates = {0}
    for k in range(1, (len(digits) - 1) // 2 + 1):
        evenIndex = 2 * k
        oddIndex = 2 * k - 1
        if evenIndex >= len(digits):
            break
        prefix = prefixes[oddIndex]
        step = denominators[oddIndex]
        for repeat in range(digits[evenIndex]):
            candidate = prefix + repeat * step
            if 0 <= candidate <= bound:
                rightCandidates.add(candidate)

    leftCandidates = {0}
    for k in range(0, (len(digits) - 2) // 2 + 1):
        index = 2 * k
        nextIndex = index + 1
        if nextIndex >= len(digits):
            break
        prefix = prefixes[index]
        step = denominators[index]
        for repeat in range(digits[nextIndex]):
            candidate = prefix + repeat * step
            if 0 <= candidate <= bound:
                leftCandidates.add(candidate)

    bestRight = 0
    bestRightGap = Decimal(1)
    for candidate in rightCandidates:
        value = decimalFraction(alpha * Decimal(candidate))
        gap = value - beta
        if gap < 0:
            gap += 1
        if gap < bestRightGap:
            bestRightGap = gap
            bestRight = candidate

    bestLeft = 0
    bestLeftGap = Decimal(1)
    for candidate in leftCandidates:
        value = decimalFraction(alpha * Decimal(candidate))
        gap = beta - value
        if gap < 0:
            gap += 1
        if gap < bestLeftGap:
            bestLeftGap = gap
            bestLeft = candidate

    return bestRight if bestRightGap < bestLeftGap else bestLeft


def bestQuadraticApproximation(d, coefficientBound, pi, piFraction):
    sqrtD = Decimal(d).sqrt()
    integerPart, period = sqrtContinuedFractionPeriod(d)
    alpha = sqrtD - Decimal(integerPart)

    positiveBound = int(((Decimal(coefficientBound) + pi) / sqrtD).to_integral_value(rounding=ROUND_FLOOR))
    positiveBound = min(max(positiveBound, 0), coefficientBound)

    negativeBound = int(((Decimal(coefficientBound) - pi) / sqrtD).to_integral_value(rounding=ROUND_FLOOR))
    negativeBound = min(max(negativeBound, 0), coefficientBound)

    positiveB = bestPositiveMultiplier(alpha, piFraction, positiveBound, period)
    negativeB = -bestPositiveMultiplier(alpha, Decimal(1) - piFraction, negativeBound, period)

    def candidatePair(b):
        realA = pi - Decimal(b) * sqrtD
        a = nearestInteger(realA)
        a = max(-coefficientBound, min(coefficientBound, a))
        error = abs(Decimal(a) + Decimal(b) * sqrtD - pi)
        return a, b, error

    positive = candidatePair(positiveB)
    negative = candidatePair(negativeB)
    return negative[:2] if negative[2] < positive[2] else positive[:2]


def piContext():
    getcontext().prec = 140
    pi = chudnovskyPi(130)
    return pi, decimalFraction(pi)


def integralPart(d, coefficientBound):
    pi, piFraction = piContext()
    a, _ = bestQuadraticApproximation(d, coefficientBound, pi, piFraction)
    return a


def integralPartSum(coefficientBound=10**13):
    pi, piFraction = piContext()
    total = 0
    for d in range(2, 100):
        if isSquare(d):
            continue
        a, _ = bestQuadraticApproximation(d, coefficientBound, pi, piFraction)
        total += abs(a)
    return total


def runTests():
    pi, piFraction = piContext()
    assert bestQuadraticApproximation(2, 10, pi, piFraction) == (6, -2)
    assert bestQuadraticApproximation(5, 100, pi, piFraction) == (-55, 26)
    assert bestQuadraticApproximation(7, 10**6, pi, piFraction) == (560_323, -211_781)
    assert bestQuadraticApproximation(2, 10**13, pi, piFraction)[0] == -6_188_084_046_055


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = integralPartSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
