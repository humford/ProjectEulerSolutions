import math
import time
from fractions import Fraction


def binaryDigit(index, value):
    if not 0 <= value < 1:
        raise ValueError("value must be in [0, 1)")
    if index <= 0:
        raise ValueError("index must be positive")

    value = Fraction(value)
    digit = 0
    for _ in range(index):
        value *= 2
        digit = int(value)
        value -= digit
    return digit


def adaptiveSimpson(function, start, end, tolerance):
    midpoint = (start + end) / 2.0
    fStart = function(start)
    fMidpoint = function(midpoint)
    fEnd = function(end)
    estimate = (end - start) * (fStart + 4.0 * fMidpoint + fEnd) / 6.0
    stack = [(start, end, fStart, fMidpoint, fEnd, estimate, tolerance)]
    total = 0.0

    while stack:
        start, end, fStart, fMidpoint, fEnd, estimate, tolerance = stack.pop()
        midpoint = (start + end) / 2.0
        leftMidpoint = (start + midpoint) / 2.0
        rightMidpoint = (midpoint + end) / 2.0

        fLeftMidpoint = function(leftMidpoint)
        fRightMidpoint = function(rightMidpoint)
        leftEstimate = (
            (midpoint - start)
            * (fStart + 4.0 * fLeftMidpoint + fMidpoint)
            / 6.0
        )
        rightEstimate = (
            (end - midpoint)
            * (fMidpoint + 4.0 * fRightMidpoint + fEnd)
            / 6.0
        )
        refined = leftEstimate + rightEstimate

        if abs(refined - estimate) <= 15.0 * tolerance:
            total += refined + (refined - estimate) / 15.0
        else:
            halfTolerance = tolerance / 2.0
            stack.append((
                midpoint,
                end,
                fMidpoint,
                fRightMidpoint,
                fEnd,
                rightEstimate,
                halfTolerance,
            ))
            stack.append((
                start,
                midpoint,
                fStart,
                fLeftMidpoint,
                fMidpoint,
                leftEstimate,
                halfTolerance,
            ))

    return total


def binarySeriesProbability(threshold):
    mean = math.pi * math.pi / 12.0
    beta = mean - threshold
    productTerms = 200
    inverseTwoSquares = [
        1.0 / (2.0 * index * index)
        for index in range(1, productTerms + 1)
    ]

    zetaFour = math.pi ** 4 / 90.0
    partialFour = sum(
        1.0 / (index ** 4)
        for index in range(1, productTerms + 1)
    )
    tailFour = zetaFour - partialFour

    def cosineProduct(t):
        product = 1.0
        for coefficient in inverseTwoSquares:
            product *= math.cos(t * coefficient)
        return product * math.exp(-t * t * tailFour / 8.0)

    def integrand(t):
        if t == 0.0:
            return beta
        return math.sin(beta * t) * cosineProduct(t) / t

    integral = adaptiveSimpson(integrand, 0.0, 1200.0, 1e-12)
    return 0.5 + integral / math.pi


def roundedBinarySeriesProbability(threshold):
    return f"{binarySeriesProbability(threshold):.8f}"


def runTests():
    assert binaryDigit(2, Fraction(1, 4)) == 1
    for index in range(1, 20):
        if index != 2:
            assert binaryDigit(index, Fraction(1, 4)) == 0


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedBinarySeriesProbability(0.5)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
