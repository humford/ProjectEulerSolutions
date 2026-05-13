from collections import Counter
from math import lcm
import time


TARGET = 1_000_000
MODULUS = 999_999_893


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))
    primes = []
    factors[0] = 0
    factors[1] = 1

    for value in range(2, limit + 1):
        if factors[value] == value:
            primes.append(value)

        for prime in primes:
            multiple = prime * value
            if multiple > limit or prime > factors[value]:
                break
            factors[multiple] = prime

    return factors


SMALL_FACTORS = smallestPrimeFactors(2 * TARGET + 2)


def factorization(value):
    factors = {}
    while value > 1:
        prime = SMALL_FACTORS[value]
        exponent = 0
        while value % prime == 0:
            value //= prime
            exponent += 1
        factors[prime] = exponent
    return factors


def divisorsFromFactors(factors):
    divisors = [1]
    for prime, exponent in factors.items():
        current = []
        power = 1
        for _ in range(exponent + 1):
            for divisor in divisors:
                current.append(divisor * power)
            power *= prime
        divisors = current
    return sorted(divisors)


def fibonacciPair(index, modulus):
    if index == 0:
        return (0, 1)

    a, b = fibonacciPair(index // 2, modulus)
    c = (a * ((2 * b - a) % modulus)) % modulus
    d = (a * a + b * b) % modulus
    if index % 2 == 0:
        return (c, d)
    return (d, (c + d) % modulus)


def pisanoPrime(prime):
    if prime == 2:
        return 3
    if prime == 5:
        return 20

    legendre = pow(5, (prime - 1) // 2, prime)
    candidate = prime - 1 if legendre == 1 else 2 * (prime + 1)
    period = candidate

    for factor in factorization(candidate):
        while period % factor == 0 and fibonacciPair(period // factor, prime) == (0, 1):
            period //= factor

    return period


PISANO_PRIME_CACHE = {}


def pisanoPrimePower(prime, exponent):
    if prime == 2:
        return 3 if exponent == 1 else 3 * (2 ** (exponent - 1))
    if prime == 5:
        candidate = 20 * (5 ** (exponent - 1))
    else:
        primePeriod = PISANO_PRIME_CACHE.setdefault(prime, pisanoPrime(prime))
        candidate = primePeriod * (prime ** (exponent - 1))

    modulus = prime**exponent
    period = candidate
    for factor in factorization(candidate):
        while (
            period % factor == 0
            and fibonacciPair(period // factor, modulus) == (0, 1)
        ):
            period //= factor

    return period


def pAdicValuation(value, prime, limit):
    if value == 0:
        return limit

    valuation = 0
    while valuation < limit and value % prime == 0:
        value //= prime
        valuation += 1
    return valuation


def fixedStateCount(prime, exponent, period):
    wideModulus = prime ** (2 * exponent)
    current, following = fibonacciPair(period, wideModulus)
    previous = (following - current) % wideModulus
    entries = [
        (previous - 1) % wideModulus,
        current % wideModulus,
        current % wideModulus,
        (following - 1) % wideModulus,
    ]

    firstInvariant = min(pAdicValuation(entry, prime, exponent) for entry in entries)
    determinant = (entries[0] * entries[3] - entries[1] * entries[2]) % wideModulus
    determinantValuation = pAdicValuation(determinant, prime, 2 * exponent)
    secondInvariant = max(determinantValuation - firstInvariant, 0)

    return prime ** (
        min(firstInvariant, exponent) + min(secondInvariant, exponent)
    )


def kernelPrimePowerDistribution(prime, exponent):
    period = pisanoPrimePower(prime, exponent)
    exactCounts = {}
    for divisor in divisorsFromFactors(factorization(period)):
        count = fixedStateCount(prime, exponent, divisor)
        for smallerPeriod, smallerCount in exactCounts.items():
            if divisor % smallerPeriod == 0:
                count -= smallerCount
        if count:
            exactCounts[divisor] = count
    return Counter(exactCounts)


def tonelliShanks(value, prime):
    if value == 0:
        return 0
    if prime == 2:
        return value
    if prime % 4 == 3:
        return pow(value, (prime + 1) // 4, prime)

    oddPart = prime - 1
    twoPower = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        twoPower += 1

    nonResidue = 2
    while pow(nonResidue, (prime - 1) // 2, prime) != prime - 1:
        nonResidue += 1

    m = twoPower
    c = pow(nonResidue, oddPart, prime)
    t = pow(value, oddPart, prime)
    root = pow(value, (oddPart + 1) // 2, prime)

    while t != 1:
        i = 1
        power = (t * t) % prime
        while power != 1:
            power = (power * power) % prime
            i += 1

        b = pow(c, 1 << (m - i - 1), prime)
        m = i
        c = (b * b) % prime
        t = (t * c) % prime
        root = (root * b) % prime

    return root


def multiplicativeOrder(value, prime):
    order = prime - 1
    for factor in factorization(order):
        while order % factor == 0 and pow(value, order // factor, prime) == 1:
            order //= factor
    return order


def splitPrimeDistribution(prime):
    rootFive = tonelliShanks(5, prime)
    inverseTwo = (prime + 1) // 2
    lambdaOrder = multiplicativeOrder(((1 + rootFive) * inverseTwo) % prime, prime)
    muOrder = multiplicativeOrder(((1 - rootFive) * inverseTwo) % prime, prime)

    distribution = Counter({1: 1})
    distribution[lambdaOrder] += prime - 1
    distribution[muOrder] += prime - 1
    distribution[lcm(lambdaOrder, muOrder)] += (prime - 1) ** 2
    return distribution


PRIME_POWER_DISTRIBUTIONS = {}


def primitiveFullDistribution(prime, exponent):
    distribution = Counter({1: 1})
    for power in range(1, exponent + 1):
        period = pisanoPrimePower(prime, power)
        distribution[period] += prime ** (2 * power) - prime ** (2 * (power - 1))
    return distribution


def primePowerDistribution(prime, exponent):
    key = (prime, exponent)
    cached = PRIME_POWER_DISTRIBUTIONS.get(key)
    if cached is not None:
        return cached

    if prime == 2:
        distribution = primitiveFullDistribution(prime, exponent)
    elif prime != 5 and pow(5, (prime - 1) // 2, prime) == prime - 1:
        distribution = primitiveFullDistribution(prime, exponent)
    elif exponent == 1 and prime != 5:
        distribution = splitPrimeDistribution(prime)
    else:
        distribution = kernelPrimePowerDistribution(prime, exponent)

    PRIME_POWER_DISTRIBUTIONS[key] = distribution
    return distribution


def combineDistributions(left, right):
    combined = Counter()
    for leftPeriod, leftCount in left.items():
        for rightPeriod, rightCount in right.items():
            combined[lcm(leftPeriod, rightPeriod)] += leftCount * rightCount
    return combined


def periodDistribution(modulus):
    distribution = Counter({1: 1})
    for prime, exponent in factorization(modulus).items():
        distribution = combineDistributions(
            distribution, primePowerDistribution(prime, exponent)
        )
    return distribution


def s(modulus):
    return sum(
        count * period * period
        for period, count in periodDistribution(modulus).items()
    )


def S(limit, answerModulus=None):
    total = 0
    for modulus in range(1, limit + 1):
        total += s(modulus)
        if answerModulus is not None:
            total %= answerModulus
    return total


def runTests():
    assert s(3) == 513
    assert s(10) == 225_820
    assert S(3) == 542
    assert S(10) == 310_897


def solve():
    return S(TARGET, MODULUS)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
