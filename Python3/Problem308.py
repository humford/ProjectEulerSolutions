import math
import time


TARGET_PRIME_INDEX = 10001


FRACTRAN_PROGRAM = (
    (17, 91),
    (78, 85),
    (19, 51),
    (23, 38),
    (29, 33),
    (77, 29),
    (95, 23),
    (77, 19),
    (1, 17),
    (11, 13),
    (13, 11),
    (15, 2),
    (1, 7),
    (55, 1),
)


def fractranStep(number):
    for numerator, denominator in FRACTRAN_PROGRAM:
        if number * numerator % denominator == 0:
            return number * numerator // denominator

    raise RuntimeError("Fractran program halted")


def nthPrime(index):
    if index < 6:
        limit = 15
    else:
        limit = int(index * (math.log(index) + math.log(math.log(index)))) + 50

    while True:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[0] = 0
        sieve[1] = 0

        for number in range(2, math.isqrt(limit) + 1):
            if sieve[number]:
                sieve[number * number : limit + 1 : number] = b"\x00" * (
                    (limit - number * number) // number + 1
                )

        primes = [number for number, is_prime in enumerate(sieve) if is_prime]
        if len(primes) >= index:
            return primes[index - 1]

        limit *= 2


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))
    factors[1] = 1

    for number in range(2, math.isqrt(limit) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def floorDivisionRangeSum(number, start, stop):
    total = 0
    divisor = start

    while divisor <= stop:
        quotient = number // divisor
        last = min(stop, number // quotient)
        total += quotient * (last - divisor + 1)
        divisor = last + 1

    return total


def automatonStepsUntilExponent(exponent):
    smallest_factor = smallestPrimeFactors(exponent)

    def largestProperDivisor(number):
        if smallest_factor[number] == number:
            return 1

        return number // smallest_factor[number]

    steps = 0
    previous_largest_divisor = 0

    for number in range(2, exponent + 1):
        divisor = largestProperDivisor(number)
        floor_sum = floorDivisionRangeSum(number, divisor, number - 1)
        extra = 0 if number == 2 else previous_largest_divisor - 1

        steps += (
            number - 1
            + (6 * number + 2) * (number - divisor)
            + 2 * floor_sum
            + extra
        )
        previous_largest_divisor = divisor

    return steps


def fractranPrimeAutomatonSteps(prime_index):
    return automatonStepsUntilExponent(nthPrime(prime_index))


def runTests():
    number = 2
    first_terms = []

    for _ in range(6):
        number = fractranStep(number)
        first_terms.append(number)

    assert first_terms == [15, 825, 725, 1925, 2275, 425]

    number = 2
    powers = []
    for _ in range(1000):
        number = fractranStep(number)
        if number != 2 and number & (number - 1) == 0:
            powers.append(number)
            if len(powers) == 3:
                break

    assert powers == [4, 8, 32]
    assert nthPrime(6) == 13


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fractranPrimeAutomatonSteps(TARGET_PRIME_INDEX)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
