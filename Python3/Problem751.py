import time
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP, getcontext


getcontext().prec = 120


def floorInteger(value):
    return int(value.to_integral_value(rounding=ROUND_FLOOR))


def generatedSequence(theta, count):
    b = theta
    terms = []
    for _ in range(count):
        a = floorInteger(b)
        terms.append(a)
        b = Decimal(a) * (b - Decimal(a) + 1)
    return terms


def concatenationValue(theta, fractionalDigits):
    b = theta
    a = floorInteger(b)
    text = str(a) + "."
    producedDigits = 0

    while producedDigits < fractionalDigits:
        b = Decimal(a) * (b - Decimal(a) + 1)
        a = floorInteger(b)
        part = str(a)
        text += part
        producedDigits += len(part)

    decimalPoint = text.index(".")
    return Decimal(text[: decimalPoint + 1 + fractionalDigits])


def fixedPointTheta(iterations=30, guardDigits=90):
    theta = Decimal("2.2")
    for _ in range(iterations):
        theta = concatenationValue(theta, guardDigits)
    return theta


def roundedTheta():
    theta = fixedPointTheta()
    quantum = Decimal("0." + "0" * 23 + "1")
    return format(theta.quantize(quantum, rounding=ROUND_HALF_UP), "f")


def runTests():
    assert generatedSequence(Decimal("2.956938891377988"), 10) == [
        2,
        3,
        5,
        8,
        13,
        21,
        34,
        55,
        89,
        144,
    ]
    assert str(concatenationValue(Decimal("2.956938891377988"), 13)).startswith(
        "2.3581321345589"
    )


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedTheta()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
