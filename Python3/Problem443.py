import math
import time


LIMIT = 10**15


def distinctPrimeFactors(number):
    factors = []
    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)

            while number % divisor == 0:
                number //= divisor

        divisor += 1 if divisor == 2 else 2

    if number > 1:
        factors.append(number)

    return factors


def gcdSequence(index=LIMIT):
    n = 4
    value = 13
    difference = value - n

    while n < index:
        target = difference - 1
        nextEvent = index + 1

        for factor in distinctPrimeFactors(target):
            candidate = (n // factor + 1) * factor

            if candidate < nextEvent:
                nextEvent = candidate

        if nextEvent > index:
            value += index - n
            break

        value += nextEvent - n - 1
        n = nextEvent - 1
        jump = math.gcd(nextEvent, target)
        value += jump
        n = nextEvent
        difference += jump - 1

    return value


def runTests():
    assert gcdSequence(20) == 60
    assert gcdSequence(1_000) == 2524
    assert gcdSequence(1_000_000) == 2624152


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gcdSequence()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
