from fractions import Fraction
import time


def tracePolynomialValue(days, x):
    if days == 0:
        return 2.0
    previous = 2.0
    current = 1.0 - x
    if days == 1:
        return current

    oneMinusX = 1.0 - x
    xOneMinusX = x * oneMinusX
    for _ in range(2, days + 1):
        previous, current = current, oneMinusX * current + xOneMinusX * previous
    return current


def integrand(days, x):
    if x == 0.0:
        return 0.0
    return (1.0 - tracePolynomialValue(days, x)) / x


def simpson(widthStart, widthEnd, startValue, endValue, midpointValue):
    return (widthEnd - widthStart) * (startValue + 4.0 * midpointValue + endValue) / 6.0


def adaptiveSimpson(days, tolerance):
    start = 0.0
    end = 1.0
    midpoint = 0.5
    startValue = integrand(days, start)
    endValue = integrand(days, end)
    midpointValue = integrand(days, midpoint)
    whole = simpson(start, end, startValue, endValue, midpointValue)

    total = 0.0
    stack = [(start, end, startValue, endValue, midpointValue, whole, tolerance, 0)]
    while stack:
        start, end, startValue, endValue, midpointValue, whole, tolerance, depth = stack.pop()
        midpoint = (start + end) / 2.0
        leftMidpoint = (start + midpoint) / 2.0
        rightMidpoint = (midpoint + end) / 2.0
        leftMidpointValue = integrand(days, leftMidpoint)
        rightMidpointValue = integrand(days, rightMidpoint)
        left = simpson(start, midpoint, startValue, midpointValue, leftMidpointValue)
        right = simpson(midpoint, end, midpointValue, endValue, rightMidpointValue)
        correction = left + right - whole

        if depth > 40 or abs(correction) <= 15.0 * tolerance:
            total += left + right + correction / 15.0
        else:
            stack.append((
                midpoint,
                end,
                midpointValue,
                endValue,
                rightMidpointValue,
                right,
                tolerance / 2.0,
                depth + 1,
            ))
            stack.append((
                start,
                midpoint,
                startValue,
                midpointValue,
                leftMidpointValue,
                left,
                tolerance / 2.0,
                depth + 1,
            ))

    return total


def expectedEmperorsExactSmall(days):
    firstPolynomial = [2]
    secondPolynomial = [1, -1]
    if days == 0:
        polynomial = firstPolynomial
    elif days == 1:
        polynomial = secondPolynomial
    else:
        for degree in range(2, days + 1):
            polynomial = [0] * (degree + 1)
            for index, coefficient in enumerate(secondPolynomial):
                polynomial[index] += coefficient
                polynomial[index + 1] -= coefficient
            for index, coefficient in enumerate(firstPolynomial):
                polynomial[index + 1] += coefficient
                polynomial[index + 2] -= coefficient
            firstPolynomial, secondPolynomial = secondPolynomial, polynomial

    integral = Fraction(0)
    for exponent, coefficient in enumerate(polynomial[1:], start=1):
        integral += Fraction(coefficient, exponent)
    return -days * integral


def expectedEmperorsValue(days):
    return days * adaptiveSimpson(days, 1e-11 if days < 1_000 else 1e-10)


def expectedEmperors(days):
    return f"{expectedEmperorsValue(days):.4f}"


def runTests():
    assert expectedEmperorsExactSmall(2) == 1
    assert expectedEmperorsExactSmall(5) == Fraction(31, 6)
    assert expectedEmperors(365) == "1174.3501"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedEmperors(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
