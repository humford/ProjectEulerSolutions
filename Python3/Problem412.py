import math
import time


MODULUS = 76_543_217
M = 10_000
N = 5_000


def rowLengths(m, n):
    return [m] * (m - n) + [m - n] * n


def exactGnomonNumberings(m, n):
    rows = rowLengths(m, n)
    cells = sum(rows)
    hookProduct = 1

    for rowIndex, rowLength in enumerate(rows):
        for column in range(rowLength):
            below = sum(1 for laterRow in rows[rowIndex + 1 :] if laterRow > column)
            right = rowLength - column - 1
            hookProduct *= right + below + 1

    return math.factorial(cells) // hookProduct


def factorialModulo(number, modulus):
    if number > modulus // 2:
        tail = 1

        for value in range(number + 1, modulus):
            tail = tail * value % modulus

        return -pow(tail, modulus - 2, modulus) % modulus

    result = 1

    for value in range(1, number + 1):
        result = result * value % modulus

    return result


def hookProductModulo(m, n, modulus):
    short = m - n
    cutout = n
    product = 1

    for diagonal in range(2 * short - 1):
        count = diagonal + 1 if diagonal < short else 2 * short - 1 - diagonal
        product = product * pow(2 * m - 1 - diagonal, count, modulus) % modulus

    for diagonal in range(short + cutout - 1):
        low = max(0, diagonal - (cutout - 1))
        high = min(short - 1, diagonal)
        count = max(0, high - low + 1)
        product = product * pow(m - 1 - diagonal, 2 * count, modulus) % modulus

    return product


def gnomonNumberingsModulo(m=M, n=N, modulus=MODULUS):
    cells = m * m - n * n
    numerator = factorialModulo(cells, modulus)
    denominator = hookProductModulo(m, n, modulus)

    return numerator * pow(denominator, modulus - 2, modulus) % modulus


def runTests():
    assert exactGnomonNumberings(3, 0) == 42
    assert exactGnomonNumberings(5, 3) == 250250
    assert exactGnomonNumberings(6, 3) == 406029023400
    assert gnomonNumberingsModulo(10, 5) == 61251715


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gnomonNumberingsModulo()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
