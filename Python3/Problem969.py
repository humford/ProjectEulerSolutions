from math import factorial
import time


TARGET = 10**18
MODULUS = 1_000_000_007


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0

    for value in range(2, int(limit**0.5) + 1):
        if sieve[value]:
            start = value * value
            sieve[start : limit + 1 : value] = b"\x00" * (
                (limit - start) // value + 1
            )

    return [value for value in range(2, limit + 1) if sieve[value]]


def sumPowers(limit, power, modulus):
    degree = power + 1
    if limit <= degree:
        return sum(pow(value, power, modulus) for value in range(1, limit + 1)) % modulus

    values = [0] * (degree + 1)
    for value in range(1, degree + 1):
        values[value] = (values[value - 1] + pow(value, power, modulus)) % modulus

    factorials = [1] * (degree + 1)
    for value in range(1, degree + 1):
        factorials[value] = factorials[value - 1] * value % modulus

    inverseFactorials = [1] * (degree + 1)
    inverseFactorials[degree] = pow(factorials[degree], modulus - 2, modulus)
    for value in range(degree, 0, -1):
        inverseFactorials[value - 1] = inverseFactorials[value] * value % modulus

    x = limit % modulus
    prefix = [1] * (degree + 1)
    for value in range(1, degree + 1):
        prefix[value] = prefix[value - 1] * (x - (value - 1)) % modulus

    suffix = [1] * (degree + 2)
    for value in range(degree, -1, -1):
        suffix[value] = suffix[value + 1] * (x - value) % modulus

    result = 0
    for value in range(degree + 1):
        numerator = prefix[value] * suffix[value + 1] % modulus
        denominator = factorials[value] * factorials[degree - value] % modulus
        if (degree - value) % 2:
            denominator = -denominator % modulus
        result += values[value] * numerator * pow(denominator, modulus - 2, modulus)
        result %= modulus

    return result


def minimalIntegralStep(k, primes):
    if k == 0:
        return 1

    step = 1
    for prime in primes:
        if prime > k:
            break

        valuation = 0
        primePower = prime
        while primePower <= k:
            valuation += k // primePower
            primePower *= prime

        exponent = (valuation + k - 1) // k
        step *= prime**exponent

    return step


def S(n):
    total = 0
    for k in range(n):
        numerator = (n - k) ** k
        denominator = factorial(k)
        if numerator % denominator == 0:
            term = numerator // denominator
            total += -term if k % 2 else term
    return total


def sumSUpTo(limit):
    primes = primesUpTo(1000)
    factorials = [1]
    total = 0
    k = 0

    while True:
        step = minimalIntegralStep(k, primes)
        if step > limit:
            break

        if k == 0:
            termLimit = limit
        else:
            termLimit = (limit - k) // step
            if termLimit <= 0:
                k += 1
                continue

        while len(factorials) <= k:
            factorials.append(factorials[-1] * len(factorials) % MODULUS)

        if k == 0:
            coefficient = 1
        else:
            coefficient = (
                pow(step % MODULUS, k, MODULUS)
                * pow(factorials[k], MODULUS - 2, MODULUS)
            ) % MODULUS
            if k % 2:
                coefficient = -coefficient % MODULUS

        total = (total + coefficient * sumPowers(termLimit, k, MODULUS)) % MODULUS
        k += 1

    return total


def solve():
    return sumSUpTo(TARGET)


def runTests():
    assert S(1) == 1
    assert S(3) == -1
    assert sum(S(value) for value in range(1, 11)) == 43
    assert sumSUpTo(10) == 43


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
