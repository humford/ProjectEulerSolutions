import time


MOD_FIVE = 5 ** 5
MOD_TEN = 10 ** 5


def unitPrefixProducts():
    products = [1] * MOD_FIVE
    product = 1

    for n in range(1, MOD_FIVE):
        if n % 5 != 0:
            product = product * n % MOD_FIVE
        products[n] = product

    return products, product


UNIT_PREFIX, UNIT_BLOCK_PRODUCT = unitPrefixProducts()


def fiveFreeFactorial(n):
    if n == 0:
        return 1

    return (
        pow(UNIT_BLOCK_PRODUCT, n // MOD_FIVE, MOD_FIVE)
        * UNIT_PREFIX[n % MOD_FIVE]
        * fiveFreeFactorial(n // 5)
    ) % MOD_FIVE


def primeFactorialExponent(n, prime):
    exponent = 0
    while n:
        n //= prime
        exponent += n
    return exponent


def combineWithZeroModulo32(remainder_mod_3125):
    multiplier = remainder_mod_3125 * pow(32, -1, MOD_FIVE) % MOD_FIVE
    return 32 * multiplier % MOD_TEN


def lastFiveNonzeroDigits(n):
    five_count = primeFactorialExponent(n, 5)
    remainder = fiveFreeFactorial(n)
    remainder = remainder * pow(pow(2, -1, MOD_FIVE), five_count, MOD_FIVE) % MOD_FIVE
    return combineWithZeroModulo32(remainder)


def runTests():
    assert lastFiveNonzeroDigits(10) == 36288
    assert lastFiveNonzeroDigits(100) == 16864
    assert lastFiveNonzeroDigits(1000) == 53472


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lastFiveNonzeroDigits(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer).zfill(5) + " in " + str(elapsed) + " seconds.")
