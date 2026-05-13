import time

import numpy


INDEX = 10**18
ORDER = 2000
MODULUS = 20092010


def multiplyPolynomials(left, right):
    product = numpy.convolve(left, right) % MODULUS
    reduced = product[:ORDER].copy()
    high = product[ORDER:]

    reduced[: ORDER - 1] = (reduced[: ORDER - 1] + high) % MODULUS
    reduced[1:ORDER] = (reduced[1:ORDER] + high) % MODULUS
    return reduced


def laggedFibonacci(index):
    coefficients = numpy.zeros(ORDER, dtype=numpy.int64)
    coefficients[0] = 1
    base = numpy.zeros(ORDER, dtype=numpy.int64)
    base[1] = 1

    while index:
        if index & 1:
            coefficients = multiplyPolynomials(coefficients, base)

        index //= 2
        if index:
            base = multiplyPolynomials(base, base)

    return int(coefficients.sum() % MODULUS)


def directLaggedFibonacci(index):
    values = [1] * ORDER

    for position in range(ORDER, index + 1):
        values.append((values[position - ORDER] + values[position - ORDER + 1]) % MODULUS)

    return values[index]


def runTests():
    for index in (0, 1, 1999, 2000, 2001, 5000):
        assert laggedFibonacci(index) == directLaggedFibonacci(index)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = laggedFibonacci(INDEX)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
