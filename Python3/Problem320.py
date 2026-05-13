import time


LIMIT = 1_000_000
POWER = 1234567890
MODULUS = 10**18


def smallestPrimeFactors(limit):
    spf = list(range(limit + 1))

    for number in range(2, int(limit**0.5) + 1):
        if spf[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if spf[multiple] == multiple:
                    spf[multiple] = number

    return spf


def factorialPrimeExponent(number, prime):
    total = 0

    while number > 0:
        number //= prime
        total += number

    return total


def inverseLegendreUpperBound(prime, target):
    base = target * (prime - 1)
    return base + prime * (target.bit_length() + 2)


def inverseFactorialPrimeExponent(prime, target, high):
    low = target * (prime - 1)

    while low < high:
        middle = (low + high) // 2

        if factorialPrimeExponent(middle, prime) >= target:
            high = middle
        else:
            low = middle + 1

    return low


def divisibleFactorialSum(limit=LIMIT, modulus=MODULUS):
    spf = smallestPrimeFactors(limit)
    factorialExponents = [0] * (limit + 1)
    currentMaximum = 0
    total = 0

    for number in range(2, limit + 1):
        remaining = number

        while remaining > 1:
            prime = spf[remaining]
            exponent = 0

            while remaining % prime == 0:
                remaining //= prime
                exponent += 1

            factorialExponents[prime] += exponent
            target = factorialExponents[prime] * POWER
            upperBound = inverseLegendreUpperBound(prime, target)

            if upperBound > currentMaximum:
                candidate = inverseFactorialPrimeExponent(prime, target, upperBound)

                if candidate > currentMaximum:
                    currentMaximum = candidate

        if number >= 10:
            total = (total + currentMaximum) % modulus

    return total


def runTests():
    assert divisibleFactorialSum(1000) == 614538266565663


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisibleFactorialSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
