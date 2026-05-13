from functools import lru_cache
import time


MODULUS = 1_000_000_007


def baseIMinusOne(real, imag):
    if real == 0 and imag == 0:
        return "0"

    digits = []
    while real or imag:
        digit = (real + imag) & 1
        digits.append(str(digit))
        real, imag = (imag - real + digit) // 2, (-real - imag + digit) // 2

    return "".join(reversed(digits))


def ceilDiv(numerator, denominator):
    return -((-numerator) // denominator)


def rectanglePointCount(xMin, xMax, yMin, yMax):
    if xMin > xMax or yMin > yMax:
        return 0

    return (xMax - xMin + 1) * (yMax - yMin + 1)


@lru_cache(maxsize=None)
def rectangleDigitOneSum(xMin, xMax, yMin, yMax):
    if xMin > xMax or yMin > yMax:
        return 0

    if xMin == xMax == yMin == yMax == 0:
        return 0

    total = 0

    for lowBit in (0, 1):
        for highBit in (0, 1):
            offsetReal = lowBit - highBit
            offsetImag = highBit

            nextXMin = ceilDiv(offsetImag - yMax, 2)
            nextXMax = (offsetImag - yMin) // 2
            nextYMin = ceilDiv(xMin - offsetReal, 2)
            nextYMax = (xMax - offsetReal) // 2

            pointCount = rectanglePointCount(nextXMin, nextXMax, nextYMin, nextYMax)
            if pointCount == 0:
                continue

            total += (lowBit + highBit) * pointCount
            total += rectangleDigitOneSum(nextXMin, nextXMax, nextYMin, nextYMax)
            total %= MODULUS

    return total


def digitOneSum(limit):
    rectangleDigitOneSum.cache_clear()
    return rectangleDigitOneSum(-limit, limit, -limit, limit)


def runTests():
    assert baseIMinusOne(11, 24) == "111010110001101"
    assert baseIMinusOne(24, -11) == "110010110011"
    assert baseIMinusOne(8, 0) == "111000000"
    assert baseIMinusOne(-5, 0) == "11001101"
    assert baseIMinusOne(0, 0) == "0"
    assert baseIMinusOne(11, 24).count("1") == 9
    assert baseIMinusOne(24, -11).count("1") == 7
    assert digitOneSum(500) == 10_795_060


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = digitOneSum(10**15)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
