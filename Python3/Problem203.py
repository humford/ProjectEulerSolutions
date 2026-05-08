import math
import time


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(limit + 1) if sieve[number]]


def pascalCoefficients(rows):
    coefficients = set()
    row = [1]

    for _ in range(rows):
        coefficients.update(row)
        row = [1] + [row[index] + row[index + 1] for index in range(len(row) - 1)] + [1]

    return coefficients


def isSquarefree(number, primes):
    for prime in primes:
        square = prime * prime
        if square > number:
            break
        if number % square == 0:
            return False

    return True


def squarefreeCoefficientSum(rows):
    coefficients = pascalCoefficients(rows)
    primes = primesUpTo(math.isqrt(max(coefficients)))
    return sum(coefficient for coefficient in coefficients if isSquarefree(coefficient, primes))


def runTests():
    assert squarefreeCoefficientSum(8) == 105


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squarefreeCoefficientSum(51)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
