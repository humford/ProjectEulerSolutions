import cmath
from math import cos, e, factorial, floor, fmod, log, log10, pi
import time


TARGET = 10**6


def expectedHSmall(n):
    return sum(
        (-1) ** k * (n - k) ** k * e ** (n - k) / factorial(k)
        for k in range(n)
    )


def firstEightNonSixDigits(value):
    fraction = value - floor(value)
    digits = []

    for _ in range(100):
        fraction *= 10
        digit = int(floor(fraction))
        fraction -= digit
        if digit != 6:
            digits.append(str(digit))
            if len(digits) == 8:
                return "".join(digits)

    raise RuntimeError("Increase digit search bound.")


def dominantCharacteristicRoot():
    root = complex(-2.0, 7.5)

    for _ in range(30):
        exponential = cmath.exp(-root)
        root -= (root - 1 + exponential) / (1 - exponential)

    return root


def firstEightNonSixDigitsLarge(n):
    root = dominantCharacteristicRoot()
    rootAbs = abs(root)
    rootArg = cmath.phase(root)

    theta = fmod(root.imag * n - rootArg, 2 * pi)
    if theta > pi:
        theta -= 2 * pi
    elif theta < -pi:
        theta += 2 * pi

    cosine = cos(theta)
    logCorrection = (
        log10(2 / rootAbs)
        + (root.real * n) / log(10)
        + log10(abs(cosine))
    )
    leadingSixes = floor(-logCorrection)
    scaledCorrection = (1 if cosine > 0 else -1) * 10 ** (logCorrection + leadingSixes)

    return firstEightNonSixDigits(2 / 3 + scaledCorrection)


def solve():
    return firstEightNonSixDigitsLarge(TARGET)


def runTests():
    assert firstEightNonSixDigits(expectedHSmall(2)) == "70774270"
    assert firstEightNonSixDigits(expectedHSmall(3)) == "55395558"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + answer + " in " + str(elapsed) + " seconds.")
