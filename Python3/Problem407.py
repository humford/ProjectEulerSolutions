import time
from array import array


LIMIT = 10**7


def smallestPrimeFactors(limit):
    factors = array("I", range(limit + 1))

    for number in range(2, int(limit**0.5) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def primePowerFactors(number, smallestFactors):
    factors = []

    while number > 1:
        prime = smallestFactors[number]
        primePower = 1

        while number % prime == 0:
            number //= prime
            primePower *= prime

        factors.append(primePower)

    return factors


def idempotentMaximum(number, smallestFactors):
    factors = primePowerFactors(number, smallestFactors)

    if number == 1:
        return 0
    if len(factors) == 1:
        return 1

    divisors = [1]

    for factor in factors:
        divisors += [value * factor for value in divisors]

    best = 1

    for divisor in divisors[1:-1]:
        other = number // divisor
        candidate = (divisor * pow(divisor, -1, other)) % number

        if candidate > best:
            best = candidate

    return best


def idempotentSum(limit=LIMIT):
    smallestFactors = smallestPrimeFactors(limit)
    return sum(idempotentMaximum(number, smallestFactors) for number in range(1, limit + 1))


def runTests():
    smallestFactors = smallestPrimeFactors(10)
    assert idempotentMaximum(1, smallestFactors) == 0
    assert idempotentMaximum(6, smallestFactors) == 4
    assert sum(idempotentMaximum(number, smallestFactors) for number in range(1, 11)) == 17


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = idempotentSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
