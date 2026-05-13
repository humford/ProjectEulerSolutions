import time


MERSENNE_60_FACTORS = {
    3: 2,
    5: 2,
    7: 1,
    11: 1,
    13: 1,
    31: 1,
    41: 1,
    61: 1,
    151: 1,
    331: 1,
    1321: 1,
}


def divisorsFromFactorization(factors):
    divisors = [1]
    for prime, exponent in factors.items():
        divisors = [divisor * prime ** power for divisor in divisors for power in range(exponent + 1)]
    return divisors


def multiplicativeOrderOfTwo(modulus):
    if modulus == 1:
        return 1
    value = 2 % modulus
    order = 1
    while value != 1:
        value = (value * 2) % modulus
        order += 1
    return order


def riffleShufflePeriod(deck_size):
    return multiplicativeOrderOfTwo(deck_size - 1)


def riffleShuffleDeckSum(period):
    factorization = {3: 1, 5: 1, 17: 1} if period == 8 else MERSENNE_60_FACTORS
    return sum(divisor + 1 for divisor in divisorsFromFactorization(factorization) if multiplicativeOrderOfTwo(divisor) == period)


def runTests():
    assert riffleShufflePeriod(52) == 8
    assert riffleShufflePeriod(86) == 8
    assert riffleShuffleDeckSum(8) == 412
    product = 1
    for prime, exponent in MERSENNE_60_FACTORS.items():
        product *= prime ** exponent
    assert product == 2 ** 60 - 1


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = riffleShuffleDeckSum(60)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
