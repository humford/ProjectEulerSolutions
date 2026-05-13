import math
import time


LIMIT = 100_000_000
MODULUS = 1_000_000_007
EXPONENT_MODULUS = MODULUS - 1


def gaussFactorial(n):
    result = 1
    for k in range(1, n):
        if math.gcd(k, n) == 1:
            result *= k
    return result


def productGaussFactorials(limit):
    result = 1
    for n in range(1, limit + 1):
        result *= gaussFactorial(n)
    return result


def mobiusSieve(limit):
    # Encoded as 0 -> 0, 1 -> +1, 2 -> -1.
    mu = bytearray(limit + 1)
    mu[1] = 1
    composite = bytearray(limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if not composite[number]:
            primes.append(number)
            mu[number] = 2

        muNumber = mu[number]
        for prime in primes:
            product = number * prime
            if product > limit:
                break
            composite[product] = 1
            if number % prime == 0:
                break
            if muNumber == 1:
                mu[product] = 2
            elif muNumber == 2:
                mu[product] = 1

    return mu


def quotientRanges(limit):
    ranges = []
    low = 1
    while low <= limit:
        quotient = limit // low
        high = limit // quotient
        ranges.append((low, high, quotient))
        low = high + 1
    return ranges


def superfactorialsAt(keys):
    values = {}
    keys = sorted(set(keys))
    position = 0
    factorial = 1
    superfactorial = 1

    if keys and keys[0] == 0:
        values[0] = 1
        position = 1

    if not keys:
        return values

    for value in range(1, keys[-1] + 1):
        factorial = factorial * value % MODULUS
        superfactorial = superfactorial * factorial % MODULUS
        while position < len(keys) and keys[position] == value:
            values[value] = superfactorial
            position += 1

    return values


def productGaussFactorialsMod(limit):
    mu = mobiusSieve(limit)
    ranges = quotientRanges(limit)
    superfactorials = superfactorialsAt(quotient - 1 for _, _, quotient in ranges)

    result = 1
    for low, high, quotient in ranges:
        exponent = quotient * (quotient - 1) // 2 % EXPONENT_MODULUS
        positiveProduct = 1
        negativeProduct = 1
        muSum = 0

        for d in range(low, high + 1):
            sign = mu[d]
            if sign == 1:
                positiveProduct = positiveProduct * d % MODULUS
                muSum += 1
            elif sign == 2:
                negativeProduct = negativeProduct * d % MODULUS
                muSum -= 1

        if exponent:
            result = result * pow(positiveProduct, exponent, MODULUS) % MODULUS
            result = result * pow(negativeProduct, (-exponent) % EXPONENT_MODULUS, MODULUS) % MODULUS

        superfactorialPower = muSum % EXPONENT_MODULUS
        if superfactorialPower:
            result = (
                result
                * pow(superfactorials[quotient - 1], superfactorialPower, MODULUS)
                % MODULUS
            )

    return result


def runTests():
    assert gaussFactorial(10) == 189
    assert productGaussFactorials(10) == 23_044_331_520_000
    assert productGaussFactorialsMod(10) == 331_358_692


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = productGaussFactorialsMod(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
