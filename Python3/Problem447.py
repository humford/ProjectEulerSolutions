import time
from array import array
from math import isqrt


MODULUS = 1_000_000_007
PROBLEM_LIMIT = 10**14


def retractionCountFromFactorPowers(factorPowers):
    product = 1
    number = 1

    for primePower in factorPowers:
        product *= 1 + primePower
        number *= primePower

    return product - number


def sumIntegers(first, last):
    return ((first + last) * (last - first + 1) // 2) % MODULUS


def mobiusAndDivisorPrefix(limit):
    mu = array("b", [0]) * (limit + 1)
    mu[1] = 1

    sigma = array("I", [0]) * (limit + 1)
    sigma[1] = 1

    primePower = array("I", [0]) * (limit + 1)
    primePower[1] = 1

    sigmaCore = array("I", [0]) * (limit + 1)
    sigmaCore[1] = 1

    isComposite = bytearray(limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            mu[number] = -1
            primePower[number] = number
            sigmaCore[number] = 1
            sigma[number] = 1 + number

        for prime in primes:
            composite = number * prime
            if composite > limit:
                break

            isComposite[composite] = 1

            if number % prime == 0:
                mu[composite] = 0
                nextPower = primePower[number] * prime
                primePower[composite] = nextPower
                sigmaCore[composite] = sigmaCore[number]
                sigma[composite] = (
                    sigmaCore[composite] * ((nextPower * prime - 1) // (prime - 1))
                )
                break

            mu[composite] = -mu[number]
            primePower[composite] = prime
            sigmaCore[composite] = sigma[number]
            sigma[composite] = sigma[number] * (1 + prime)

    divisorPrefix = array("I", [0]) * (limit + 1)
    total = 0

    for number in range(1, limit + 1):
        total = (total + sigma[number]) % MODULUS
        divisorPrefix[number] = total

    return mu, divisorPrefix


def divisorSummatory(limit, divisorPrefix):
    if limit < len(divisorPrefix):
        return divisorPrefix[limit]

    total = 0
    start = 1

    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        total = (total + (quotient % MODULUS) * sumIntegers(start, end)) % MODULUS
        start = end + 1

    return total


def retractionSummatory(limit):
    root = isqrt(limit)
    mu, divisorPrefix = mobiusAndDivisorPrefix(root)
    divisorCache = {}
    total = 0

    # sigma*(n)=prod(p^e+1) and R(n)=sigma*(n)-n.
    # The identity sigma*(n)=sum_{d^2|n} mu(d)*d*sigma(n/d^2)
    # reduces the summatory function to divisor-sum prefixes up to sqrt(limit).
    for divisor in range(1, root + 1):
        if mu[divisor]:
            quotient = limit // (divisor * divisor)

            if quotient < len(divisorPrefix):
                divisorTotal = divisorPrefix[quotient]
            else:
                divisorTotal = divisorCache.get(quotient)
                if divisorTotal is None:
                    divisorTotal = divisorSummatory(quotient, divisorPrefix)
                    divisorCache[quotient] = divisorTotal

            total = (total + mu[divisor] * divisor * divisorTotal) % MODULUS

    triangular = (limit % MODULUS) * ((limit + 1) % MODULUS) * pow(2, MODULUS - 2, MODULUS)
    return (total - triangular) % MODULUS


def runTests():
    assert retractionCountFromFactorPowers([4, 3]) == 8
    assert retractionSummatory(10**7) == 638_042_271


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = retractionSummatory(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
