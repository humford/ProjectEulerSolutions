import time
from math import prod


MOD = 1_000_000_007


def firstPrimesEndingIn7(count):
    primes = [2]
    result = []
    candidate = 3
    while len(result) < count:
        limit = int(candidate ** 0.5)
        isPrime = True
        for prime in primes:
            if prime > limit:
                break
            if candidate % prime == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(candidate)
            if candidate % 10 == 7:
                result.append(candidate)
        candidate += 2
    return result


def F(k, modulus=MOD):
    primes = firstPrimesEndingIn7(k)
    productMod = 1
    phiMod = 1
    for prime in primes:
        productMod = productMod * prime % modulus
        phiMod = phiMod * (prime - 1) % modulus

    qBySubsetSizeMod4 = (7, 1, 3, 9)
    alternatingSum = 0
    binomial = 1
    for subsetSize in range(k + 1):
        term = binomial * qBySubsetSizeMod4[subsetSize % 4] % modulus
        alternatingSum = (alternatingSum - term if subsetSize % 2 else alternatingSum + term) % modulus
        if subsetSize < k:
            binomial = binomial * (k - subsetSize) % modulus
            binomial = binomial * pow(subsetSize + 1, modulus - 2, modulus) % modulus

    return productMod * ((alternatingSum + 5 * phiMod) % modulus) % modulus


def bruteF(k):
    primes = firstPrimesEndingIn7(k)
    factors = [2, 5] + primes
    limit = prod(factors)
    total = 0
    for value in range(7, limit, 10):
        if all(value % factor for factor in factors):
            total += value
    return total


def runTests():
    for k in range(1, 4):
        assert F(k) == bruteF(k)
    assert F(3) == 76_101_452


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = F(97)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
