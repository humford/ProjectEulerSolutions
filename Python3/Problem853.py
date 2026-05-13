import math
import time


def primeFactors(n):
    factors = {}
    divisor = 2

    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        divisor += 1 if divisor == 2 else 2

    if n > 1:
        factors[n] = factors.get(n, 0) + 1

    return factors


def fibonacci(n, modulus=None):
    def pair(k):
        if k == 0:
            return 0, 1
        a, b = pair(k // 2)
        if modulus is None:
            c = a * (2 * b - a)
            d = a * a + b * b
        else:
            c = a * (2 * b - a) % modulus
            d = (a * a + b * b) % modulus
        if k % 2:
            return d, (c + d) if modulus is None else (c + d) % modulus
        return c, d

    return pair(n)[0]


def lcm(a, b):
    return a // math.gcd(a, b) * b


def pisanoPeriod(n, limit):
    previous = 0
    current = 1

    for period in range(1, limit + 1):
        previous, current = current, (previous + current) % n
        if previous == 0 and current == 1:
            return period

    return None


def generateMultiples(primes, periods, maxExponents, limit):
    if not primes:
        return []

    prime = primes[0]
    period = periods[0]
    maxExponent = maxExponents[0]
    result = []
    value = 1
    valuePeriod = 1

    for exponent in range(maxExponent + 1):
        if value > 1:
            result.append((value, valuePeriod))

        if len(primes) > 1:
            for otherValue, otherPeriod in generateMultiples(
                primes[1:],
                periods[1:],
                maxExponents[1:],
                limit // value,
            ):
                combined = value * otherValue
                if combined < limit:
                    result.append((combined, lcm(valuePeriod, otherPeriod)))

        if exponent == 0:
            value *= prime
            valuePeriod *= period
        else:
            value *= prime
            valuePeriod *= prime

    return result


def sumWithPisanoPeriod(targetPeriod, limit):
    primes = []
    primePeriods = []
    maxExponents = []

    for prime in primeFactors(fibonacci(targetPeriod)):
        period = pisanoPeriod(prime, targetPeriod)
        if period is not None and targetPeriod % period == 0:
            primes.append(prime)
            primePeriods.append(period)
            exponent = 0
            liftedPeriod = period
            while targetPeriod % liftedPeriod == 0:
                liftedPeriod *= prime
                exponent += 1
            maxExponents.append(exponent)

    candidates = generateMultiples(primes, primePeriods, maxExponents, limit)
    return sum(value for value, period in candidates if period == targetPeriod)


def bruteSumWithPisanoPeriod(targetPeriod, limit):
    return sum(
        n
        for n in range(2, limit)
        if pisanoPeriod(n, targetPeriod * 10) == targetPeriod
    )


def runTests():
    assert bruteSumWithPisanoPeriod(18, 50) == 57


def solve():
    return sumWithPisanoPeriod(120, 10**9)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
