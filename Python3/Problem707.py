import time


MODULUS = 1_000_000_007


def polynomialDegree(polynomial):
    return polynomial.bit_length() - 1


def polynomialRemainder(dividend, divisor):
    divisorDegree = polynomialDegree(divisor)
    while dividend and polynomialDegree(dividend) >= divisorDegree:
        dividend ^= divisor << (polynomialDegree(dividend) - divisorDegree)
    return dividend


def polynomialGcd(a, b):
    while b:
        a, b = b, polynomialRemainder(a, b)
    return a


def polynomialMod(poly, modulusPolynomial, modulusDegree):
    while poly and polynomialDegree(poly) >= modulusDegree:
        poly ^= modulusPolynomial << (polynomialDegree(poly) - modulusDegree)
    return poly


def polynomialSquareMod(poly, modulusPolynomial, modulusDegree):
    result = 0
    bits = poly

    while bits:
        bit = bits & -bits
        exponent = bit.bit_length() - 1
        result |= 1 << (2 * exponent)
        bits ^= bit

    return polynomialMod(result, modulusPolynomial, modulusDegree)


def polynomialTimesXMod(poly, modulusPolynomial, modulusDegree):
    return polynomialMod(poly << 1, modulusPolynomial, modulusDegree)


def lightsOutRowCharacteristic(width):
    if width <= 0:
        raise ValueError("width must be positive")

    xPlusOne = 0b11
    if width == 1:
        return xPlusOne

    previous = 1
    current = xPlusOne
    for _ in range(2, width + 1):
        previous, current = current, (current << 1) ^ current ^ previous

    return current


def fibonacciPolynomialMod(index, modulusPolynomial, modulusDegree):
    if index == 0:
        return 0, 1

    current, nextValue = fibonacciPolynomialMod(index >> 1, modulusPolynomial, modulusDegree)
    currentSquared = polynomialSquareMod(current, modulusPolynomial, modulusDegree)
    nextSquared = polynomialSquareMod(nextValue, modulusPolynomial, modulusDegree)
    doubled = polynomialTimesXMod(currentSquared, modulusPolynomial, modulusDegree)
    doubledNext = currentSquared ^ nextSquared

    if index % 2 == 0:
        return doubled, doubledNext

    following = polynomialTimesXMod(doubledNext, modulusPolynomial, modulusDegree) ^ doubled
    return doubledNext, following


class LightsOutWidthSolver:
    def __init__(self, width):
        self.width = width
        self.characteristic = lightsOutRowCharacteristic(width)
        self.degree = width

    def nullity(self, height):
        if height <= 0:
            raise ValueError("height must be positive")

        fibPolynomial, _ = fibonacciPolynomialMod(height + 1, self.characteristic, self.degree)
        return polynomialDegree(polynomialGcd(self.characteristic, fibPolynomial))

    def solvableStateCount(self, height, modulus=MODULUS):
        nullity = self.nullity(height)
        exponent = self.width * height - nullity

        if modulus is None:
            return 1 << exponent
        return pow(2, exponent % (modulus - 1), modulus)


def fibonacciSequence(count):
    values = [0] * (count + 1)
    if count >= 1:
        values[1] = 1
    if count >= 2:
        values[2] = 1

    for i in range(3, count + 1):
        values[i] = values[i - 1] + values[i - 2]

    return values


def solvableStateCount(width, height, modulus=MODULUS):
    return LightsOutWidthSolver(width).solvableStateCount(height, modulus)


def fibonacciSolvableStateSum(width, count, modulus=MODULUS):
    solver = LightsOutWidthSolver(width)
    fibonacciNumbers = fibonacciSequence(count)
    total = 0

    for i in range(1, count + 1):
        total = (total + solver.solvableStateCount(fibonacciNumbers[i], modulus)) % modulus

    return total


def runTests():
    assert solvableStateCount(1, 2, modulus=None) == 2
    assert solvableStateCount(3, 3, modulus=None) == 512
    assert solvableStateCount(4, 4, modulus=None) == 4_096
    assert solvableStateCount(7, 11) == 270_016_253
    assert fibonacciSolvableStateSum(3, 3) == 32
    assert fibonacciSolvableStateSum(4, 5) == 1_052_960
    assert fibonacciSolvableStateSum(5, 7) == 346_547_294


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciSolvableStateSum(199, 199)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
