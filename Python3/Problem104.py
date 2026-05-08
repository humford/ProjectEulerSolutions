import math
import time


PANDIGITAL = set("123456789")


def isPandigital(n):
    text = str(n)
    return len(text) == 9 and set(text) == PANDIGITAL


def leadingFibonacciDigits(index, digits):
    phi = (1 + 5 ** 0.5) / 2
    log_value = index * math.log10(phi) - math.log10(5) / 2
    fractional = log_value - math.floor(log_value)
    return int(10 ** (fractional + digits - 1))


def firstPandigitalFibonacciIndex():
    modulus = 10 ** 9
    previous = 1
    current = 1
    index = 2

    while True:
        previous, current = current, (previous + current) % modulus
        index += 1

        if isPandigital(current) and isPandigital(leadingFibonacciDigits(index, 9)):
            return index


def runTests():
    assert isPandigital(123456789)
    assert not isPandigital(123456788)
    assert leadingFibonacciDigits(12, 3) == 144


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstPandigitalFibonacciIndex()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
