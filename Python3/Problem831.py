import math
import time


DEGREE = 5


def multiplyPolynomials(left, right, degree=DEGREE):
    product = [0] * (degree + 1)

    for i, leftCoefficient in enumerate(left):
        if leftCoefficient == 0:
            continue
        for j, rightCoefficient in enumerate(right):
            if rightCoefficient == 0:
                continue
            if i + j <= degree:
                product[i + j] += leftCoefficient * rightCoefficient

    return product


def powerPolynomial(poly, exponent, degree=DEGREE):
    result = [0] * (degree + 1)
    result[0] = 1
    base = list(poly)

    while exponent:
        if exponent % 2 == 1:
            result = multiplyPolynomials(result, base, degree)
        exponent //= 2
        if exponent:
            base = multiplyPolynomials(base, base, degree)

    return result


def coefficientC(m):
    # ((1+x)^7 - 1) = 7x * Q(x).  The x^6/7 term of Q cannot affect [x^5].
    q = [1, 3, 5, 5, 3, 1]
    qToM = powerPolynomial(q, m)
    onePlusXToFive = [math.comb(5, k) for k in range(DEGREE + 1)]

    return multiplyPolynomials(onePlusXToFive, qToM)[DEGREE]


def g(m):
    return 7**m * coefficientC(m)


def directG(m):
    total = 0

    for j in range(m + 1):
        for i in range(j + 1):
            sign = -1 if (j - i) % 2 else 1
            total += (
                sign
                * math.comb(m, j)
                * math.comb(j, i)
                * math.comb(j + 5 + 6 * i, j + 5)
            )

    return total


def toBase(n, base):
    if n == 0:
        return "0"

    digits = []
    while n:
        n, digit = divmod(n, base)
        digits.append(str(digit))

    return "".join(reversed(digits))


def firstBase7DigitsOfG(m, digits=10):
    coefficient = coefficientC(m)
    base7Coefficient = toBase(coefficient, 7)

    if len(base7Coefficient) >= digits:
        return base7Coefficient[:digits]

    return base7Coefficient + "0" * (digits - len(base7Coefficient))


def runTests():
    assert directG(10) == 127278262644918
    assert g(10) == 127278262644918
    assert str(g(10))[:5] == "12727"


def solve():
    return firstBase7DigitsOfG(142857)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
