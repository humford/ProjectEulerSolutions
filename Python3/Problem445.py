import time
from array import array


MODULUS = 1_000_000_007
PROBLEM_LIMIT = 10_000_000


def smallestPrimeFactors(limit):
    factors = array("I", range(limit + 1))

    for number in range(2, int(limit**0.5) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def modularInverses(limit):
    inverses = array("I", [0]) * (limit + 1)
    inverses[1] = 1

    for number in range(2, limit + 1):
        inverses[number] = (
            MODULUS - (MODULUS // number) * inverses[MODULUS % number] % MODULUS
        )

    return inverses


# The retraction conditions are n | b(a-1) and n | a(a-1).  By the Chinese
# remainder theorem this gives R(n)=prod(p^e+1)-n for n=prod(p^e).
def retractionBinomialSum(limit):
    smallestFactors = smallestPrimeFactors(limit)
    inverses = modularInverses(limit)
    exponents = array("i", [0]) * (limit + 1)
    primePowers = array("I", [1]) * (limit + 1)
    inverseTerms = array("I", [1]) * (limit + 1)
    product = 1
    zeroTerms = 0
    binomial = 1
    total = 0

    def updatePrime(prime, delta):
        nonlocal product, zeroTerms
        exponent = exponents[prime]

        if exponent:
            oldTerm = (1 + primePowers[prime]) % MODULUS
            if oldTerm:
                product = product * inverseTerms[prime] % MODULUS
            else:
                zeroTerms -= 1

        if delta > 0:
            for _ in range(delta):
                primePowers[prime] = primePowers[prime] * prime % MODULUS
        else:
            inverse = inverses[prime]
            for _ in range(-delta):
                primePowers[prime] = primePowers[prime] * inverse % MODULUS

        exponent += delta
        exponents[prime] = exponent

        if exponent:
            term = (1 + primePowers[prime]) % MODULUS
            if term:
                inverseTerms[prime] = pow(term, MODULUS - 2, MODULUS)
                product = product * term % MODULUS
            else:
                zeroTerms += 1

    def updateFactorization(number, sign):
        while number > 1:
            prime = smallestFactors[number]
            exponent = 0

            while number % prime == 0:
                number //= prime
                exponent += 1

            updatePrime(prime, sign * exponent)

    for k in range(1, limit):
        updateFactorization(limit - k + 1, 1)
        updateFactorization(k, -1)
        binomial = binomial * (limit - k + 1) % MODULUS * inverses[k] % MODULUS
        retractionCount = 0 if zeroTerms else product
        total = (total + retractionCount - binomial) % MODULUS

    return total


def runTests():
    assert retractionBinomialSum(10) == 1118
    assert retractionBinomialSum(100) == 516982162
    assert retractionBinomialSum(1_000) == 853246560
    assert retractionBinomialSum(10_000) == 772758839
    assert retractionBinomialSum(100_000) == 628701600


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = retractionBinomialSum(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
