import bisect
import math
import time


LIMIT = 190
MODULUS = 10**16


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    sieve[0] = 0
    sieve[1] = 0

    for number in range(2, math.isqrt(limit - 1) + 1):
        if sieve[number]:
            sieve[number * number : limit : number] = b"\x00" * (
                (limit - 1 - number * number) // number + 1
            )

    return [number for number in range(limit) if sieve[number]]


def subsetProducts(values):
    products = [1]

    for value in values:
        products += [product * value for product in products]

    return products


def pseudoSquareRoot(factors):
    product = math.prod(factors)
    root = math.isqrt(product)
    middle = len(factors) // 2
    left_products = subsetProducts(factors[:middle])
    right_products = sorted(subsetProducts(factors[middle:]))
    best = 0

    for left in left_products:
        if left > root:
            continue

        index = bisect.bisect_right(right_products, root // left) - 1
        if index >= 0:
            best = max(best, left * right_products[index])

    return best


def primeProductPseudoSquareRootMod(limit, modulus):
    return pseudoSquareRoot(primeSieve(limit)) % modulus


def runTests():
    assert pseudoSquareRoot([2, 2, 3]) == 3
    assert pseudoSquareRoot([2, 3, 11, 47]) == 47


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeProductPseudoSquareRootMod(LIMIT, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
