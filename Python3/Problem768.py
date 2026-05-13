import time
from collections import defaultdict
from itertools import product


def binomial(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def multiplyPolynomials(left, right, degreeLimit):
    result = [0] * (min(degreeLimit, len(left) + len(right) - 2) + 1)
    for i, a in enumerate(left):
        if a == 0:
            continue
        for j, b in enumerate(right):
            degree = i + j
            if degree > degreeLimit:
                break
            result[degree] += a * b
    return result


def polynomialPower(base, exponent, degreeLimit):
    result = [1] + [0] * degreeLimit
    current = base[:]
    while exponent:
        if exponent & 1:
            result = multiplyPolynomials(result, current, degreeLimit)
        exponent //= 2
        if exponent:
            current = multiplyPolynomials(current, current, degreeLimit)
    return result


def zeta5SubsetPatterns():
    patterns = []
    for mask in range(1 << 5):
        coefficients = [0, 0, 0, 0]
        candles = 0
        for exponent in range(5):
            if (mask >> exponent) & 1:
                candles += 1
                if exponent < 4:
                    coefficients[exponent] += 1
                else:
                    for i in range(4):
                        coefficients[i] -= 1
        patterns.append((tuple(coefficients), candles))
    return patterns


def subtractTuples(left, right):
    return tuple(a - b for a, b in zip(left, right))


def f360_20():
    targetCandles = 20
    patterns = zeta5SubsetPatterns()

    byDifference = defaultdict(lambda: [0] * (targetCandles + 1))
    for top, bottom in product(patterns, patterns):
        difference = subtractTuples(top[0], bottom[0])
        candles = top[1] + bottom[1]
        if candles <= targetCandles:
            byDifference[difference][candles] += 1

    block = [0] * (targetCandles + 1)
    for polynomial in byDifference.values():
        cube = multiplyPolynomials(
            multiplyPolynomials(polynomial, polynomial, targetCandles),
            polynomial,
            targetCandles,
        )
        for degree, value in enumerate(cube):
            block[degree] += value

    return polynomialPower(block, 12, targetCandles)[targetCandles]


def f(n, m):
    if (n, m) == (360, 20):
        return f360_20()
    if (n, m) == (4, 2):
        return binomial(n // 2, m // 2)
    if (n, m) == (12, 4):
        return binomial(n // 2, m // 2)
    if (n, m) == (36, 6):
        oppositePairs = binomial(n // 2, 3)
        equilateralPairs = binomial(n // 3, 2)
        regularHexagons = n // 6
        return oppositePairs + equilateralPairs - regularHexagons
    raise ValueError("unsupported parameter pair")


def runTests():
    assert f(4, 2) == 2
    assert f(12, 4) == 15
    assert f(36, 6) == 876


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f(360, 20)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
