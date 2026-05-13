import math
import time
from fractions import Fraction


SQUARES = 500
CROAKS = "PPPPNNPPPNPPNPN"


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    for number in range(4, limit + 1, 2):
        sieve[number] = 0

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start::step] = b"\x00" * ((limit - start) // step + 1)

    return sieve


def primeFrogProbability(squares=SQUARES, croaks=CROAKS):
    primes = primeSieve(squares)
    probabilities = [Fraction(0, 1)] + [Fraction(1, squares)] * squares

    for croak in croaks:
        nextProbabilities = [Fraction(0, 1)] * (squares + 1)

        for square in range(1, squares + 1):
            if primes[square]:
                croakProbability = Fraction(2, 3) if croak == "P" else Fraction(1, 3)
            else:
                croakProbability = Fraction(1, 3) if croak == "P" else Fraction(2, 3)

            current = probabilities[square] * croakProbability

            if square == 1:
                nextProbabilities[2] += current
            elif square == squares:
                nextProbabilities[squares - 1] += current
            else:
                nextProbabilities[square - 1] += current / 2
                nextProbabilities[square + 1] += current / 2

        probabilities = nextProbabilities

    return sum(probabilities)


def runTests():
    assert primeFrogProbability(2, "N") == Fraction(1, 2)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeFrogProbability()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
